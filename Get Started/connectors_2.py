from ares.Lib import Ares


"""
GENERAL PURPOSE
---------------

In this script we will see how to create your own connectors dynamically and run them just the same

You can have further information on this in the cheatsheet provided in the framework

"""



class MyConnector(object):
  """
  This class will be your own connector
  """

  ALIAS = 'MY_CONNECTOR'
  NEEDS_PROXY = True

  @classmethod
  def isCompatible(cls, params):
    """
    Method that the framework will use to perform a quick check when importing the connector
    """
    return (True, '')

  @classmethod
  def _getData(cls, *args, **kwargs):
    """
    You will need to return a list of dictionaries
    """
    return [{'mydata': 'something', 'number': 1}, {'mydata': 'somethingelse', 'number': 23}]


#here we make the assumption that the connector doesn't need authentication
aresObj = Ares.ReportAPI()


#The dynamic connector will need proxy settings so we set it there otherwise
aresObj.addProxy('myproxy.fr', '8080', proxyUser='random_user', proxyPass='another_pass')

#Add the dynamic connector to the framework
aresObj.addExternalConnector(MyConnector)

#Now you can call the connetor - note that if you didn't set the NEEDS_PROXY attribute you can still test it by using useProxy parameter
result = aresObj.getData('MY_CONNECTOR')

#we want to show the information extracted in a datatable
aresObj.table(result)

aresObj.html()