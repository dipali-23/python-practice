# Create a custom module with the function of converting array of string
# to dictionary of string(key as sequence integer and value as string).
# Import and use these functions from another python script to display
# output in console


def convert_to_dict(str):
    dist={}
    key=0
    for i in str:
        dist.update({key:i})
        key+=1
    return dist
