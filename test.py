from fortalezdb import *

db = init('Snehashish',
    'http://127.0.01:5000',
    'DB2',
    '4370608feaf82266fb555b5a7be062676137fe2730716ef76bc258ea320cc614')

print(create_new_table(db, 'NewTable', ['test1', 'test2', 'test3']))