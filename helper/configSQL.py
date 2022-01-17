import config

cfg = config.Config('helper/mysql.cfg')
config = {
  'user': cfg['user'],
  'password': cfg['password'],
  'host': cfg['host'],
  'database': 'china_stock_wiki',
  'raise_on_warnings': True,
  'allow_local_infile': False,
  'table_name': '',
  'windAccount': cfg['simulate_account'],
  'windPassword': cfg['simulate_password']
}
