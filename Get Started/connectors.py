from ares.Lib import Ares


"""
GENERAL PURPOSE
---------------

This script will aim to show how to use the data extraction capabilities that AReS has to offer

We will see first how to simply run a simple connection through the various interfaces that exist

In the second script we will see how to create your own connectors dynamically and run them just the same

You can have further information on this in the cheatsheet provided in the framework

"""


#if you want to use a connector that requires authentication, you will have to define the user and password in the ReportAPI constructor
aresObj = Ares.ReportAPI('user', 'pwd')

#Then if the connector you want to call requires authentication - you'll need to provide your credentials
#in the framework the key for the user will always be user_id for the already defined interfaces
aresObj.addCredentials('WEB', 'password1', {'user_id': 'user1'})

#if you need to go through a proxy to get to the internet then you can set it here
aresObj.addProxy('myproxy.fr', '8080', proxyUser='random_user', proxyPass='another_pass')

#All the above steps are not mandatory to use connectors as long as no security or authentication is required to make them work
#Regarding the proxy, all of the basics connectors will have the attribute NEEDS_PROXY set for them which gives you a clue

#getData is the single function to extract data from all the connectors
ares_df = aresObj.getData('CONNECTOR_NAME', {})

#we want to show the information extracted in a datatable
aresObj.table(ares_df)

ares_df2 = aresObj.getData('ANOTHER_CONNECTOR', {})
aresObj.chart('line', ares_df2)

aresObj.toHtml()