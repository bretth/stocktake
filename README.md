Stocktake is a small script that reconciles your recorded stock against a stock count and produces a stock adjustment file.

To install, `pip install git+https://github.com/bretth/stocktake`.

Usage:

`stocktake file1.csv file2.csv file3.csv`

The program takes 3 filename arguments. 

The first filename argument should be the current recorded stock csv file with 2 columns 'sku' and 'quantity'. Additionally you can have an optional third column which contains the primary key for the stock item. Header rows will be ignored.

The count file is a simple 'sku', 'quantity' csv file.

Stocktake creates a union set of the skus from both files and outputs the 3rd  csv file with quantity adjustments to make. The first column of the output file contains the primary key or sku. A negative quantity should be read as negative adjustment to stock. 

The program will give warnings if the quantity is invalid or in the event that primary keys are provided and there is a missing key.
