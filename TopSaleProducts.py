from mrjob.job import MRJob
from mrjob.step import MRStep
from heapq import nlargest
from operator import itemgetter

class TopSaleProducts(MRJob):

    MRJob.SORT_VALUES = True

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_orders,
                   reducer=self.reducer_count_orders),
            MRStep(reducer=self.reducer_find_top10_sold_products)
        ]

    def mapper_get_orders(self, _, line):
        # Splitting the line by semicolon and extracting required fields
        # "OrderID";"ProductID";"UnitPrice";"Quantity";"Discount"
        (orderID, productID, unitPrice, quantity, discount) = line.split(';')
        # Calculating the total sale amount for each product
        saleAmt = unitPrice * int(quantity) * (1 - float(discount))
        yield productID, saleAmt

    def reducer_count_orders(self, productID, saleAmts):
        # Calculating the total sale amount for each product
        totalSaleAmt = sum(saleAmts)
        yield None, (totalSaleAmt, productID)

    def reducer_find_top10_sold_products(self, _, saleAmtProductPairs):
        # Finding the top 10 products based on total sale amount
        top10 = nlargest(10, saleAmtProductPairs, key=itemgetter(0))
        for saleAmtProductPair in top10:
            yield saleAmtProductPair[1], saleAmtProductPair[0]

if __name__ == '__main__':
    TopSaleProducts.run()
