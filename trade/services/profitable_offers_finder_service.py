from functools import reduce

from django.db.models import QuerySet

from offer.models import Offer, BUY


class ProfitableOffersFinder:

    def __init__(self, sell_offer: Offer):
        self.sell_offer = sell_offer

    def find_the_most_profitable(self):
        """Finds the most profitable combination of buy offers
            for given sell offer"""
        buy_offers = self._get_buy_offers(exclude_user=self.sell_offer.user)

        if buy_offers.exists():
            target_quantity = self.sell_offer.entry_quantity
            subsets = list(self._subset_sum(buy_offers=buy_offers,
                                            target_quantity=target_quantity))
            print(f'All subsets: {subsets}')

            most_profitable = self._find_the_most_profitable_combination(
                subsets=subsets, average=self.sell_offer.get_avg_price())

            print(f'The most profitable: {most_profitable}')
            return most_profitable

    def _subset_sum(self, buy_offers: QuerySet, target_quantity: int,
                    suitable_offers=[], partial_sum=0) -> list:
        """Based on the recursive combinations algorithm.
        Returns all combinations of buy offers the sum of the number
        of stocks of which is equal to the target quantity or
        empty list if there are no suitable combinations.

        for example:
            target_quantity = 10
            buy_offers: [
                    offer1(quantity=5),
                    offer2(quantity=5),
                    offer3(quantity=10)]

            will return [[offer1, offer2], [offer3]]
        """
        # check if the partial sum is equals to target
        if partial_sum == target_quantity:
            yield suitable_offers

        if partial_sum >= target_quantity:
            return  # if we reach the number why bother to continue

        for index, offer in enumerate(buy_offers):
            remaining = buy_offers[index + 1:]
            yield from self._subset_sum(remaining, target_quantity,
                                        suitable_offers + [offer],
                                        partial_sum + offer.entry_quantity)

    def _find_the_most_profitable_combination(self, subsets: list,
                                              average: float):
        """Returns the most profitable combination from subsets.
        Checks that the average cost of each subset is greater than average.
        Selects the subset with the highest average cost."""
        if not subsets:
            return

        profitable_subset_index = None
        print(f'Average: {average}')

        for index, offers_list in enumerate(subsets):
            avg_for_offer_list = self._get_avg_for_subset(offers_list)
            print(f'{index} AVG for {offers_list} -> {avg_for_offer_list}')

            if avg_for_offer_list >= average:
                average = avg_for_offer_list
                profitable_subset_index = index
                print(f' Changed index: {profitable_subset_index}')

        return (subsets[profitable_subset_index] if
                profitable_subset_index is not None else None)

    def _get_avg_for_subset(self, subset):
        sum_of_prices_in_subset = reduce(lambda a, b: a + b,
                                         [offer.get_avg_price()
                                          for offer in subset])
        return sum_of_prices_in_subset / len(subset)

    def _get_buy_offers(self, exclude_user):
        return (Offer.objects.filter(order_type=BUY, is_active=True)
                .exclude(user=exclude_user))
