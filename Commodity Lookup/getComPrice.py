import requests
import urllib.parse

main_api = "https://eddb.io/archive/v6/commodities.json"

# get dump for last market data
# find the last ~5 top max-buy systems for a commodity


url = main_api 
print (url)

json_data = requests.get(url).json()

while True:
	name = input('[commodity name, list_commodities, list_all_rares, or q/quit] : ')

	if name == 'quit' or name == 'q':
		exit(0)

	if name == 'list_commodities' or name == 'list':
		commodity = input("What commodity type are you searching for? ")
		isRare = input("only rares?(y/n): ")
		if isRare == 'n':
			for each in json_data:
				if each['is_rare'] == 0:
					if each['category']['name'] == commodity:
						print("'"+ str(each['name']) + "', ")
		# exit(0)
		if isRare == 'y':
			for each in json_data:
				if each['is_rare'] == 1:
					if each['category']['name'] == commodity:
						print("'"+ str(each['name']) + "', ")
	
	if name == 'list_all_rares':
		commodity = input("What commodity type are you searching for? ")
		for each in json_data:
				if each['is_rare'] == 1:
					if each['category']['name'] == commodity:
						print(each)

	for each in json_data:
		if each['name'] == name:
			print('Max price: ' + str(each['max_sell_price']))
			print('Upper average: ' + str(each['sell_price_upper_average']))
			print('Average price: ' + str(each['average_price']))
			print('Max buy price: ' + str(each['max_buy_price']))
