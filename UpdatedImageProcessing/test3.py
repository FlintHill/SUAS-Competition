d = {
	"a": 0,
	"b": 1,
	"c": 2
}

print("before")

print(d)

del d[min(d, key=d.get)]

print("after")

print(d)