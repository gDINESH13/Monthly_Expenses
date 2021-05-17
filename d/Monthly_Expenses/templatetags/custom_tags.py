from django import template

register=template.Library()



def sub(value,val):
    return value-val

register.filter('sub',sub)