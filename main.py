from stock_data import get_stock
import json
with open('data.json', 'w') as f:
    json.dump(get_stock("lgcb"), f)
