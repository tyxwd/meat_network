import pandas
import numpy
frame = pandas.DataFrame(numpy.arange(8).reshape((2, 4)),
                         index=['three', 'one'],
                         columns=['d', 'a', 'b', 'c'])
print(frame)
fr2 = frame.sort_index()
print(frame)
print(fr2)