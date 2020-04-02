import regex
import functools

# m=regex.findall("AA", "CAG")
# m=regex.findall("(AA){e<=1}", "CAAG") # means allow up to 1 error


initial = regex.findall("(AAAC){e<=1}", "TTTGTTGATATTTAAACGGAATATTTATTGAGGGTTTATTGGTGGGGAGAAAGGGCTTGATGCCTTG", overlapped=True)
filtered = functools.reduce(lambda a,b : [*a, b] if len(b)==4 else a, initial,[])
print(filtered)