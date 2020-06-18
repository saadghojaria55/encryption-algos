def railencrypt(text, numrails):
    text = text.lower()
    rails = [text[n::numrails] for n in range(numrails)]
    return "".join(rails)

Str="Hello World"
print(railencrypt(Str,3))
