import os
from time import time
import unittest

from vehicular.main import Run
from vehicular.database import Database

MAKES = ['harley davidson', 'gsxr', 'drz', 'cbr', 'klx', 'crf', 'triumph', 'sv650', 'Honda CB750', ' Honda XR650R',
         'KTM', 'Honda CR500', 'Suzuki GSXR 1000', 'Honda CBR600', 'BMW S1000RR', 'Aprilia RSV4',
         'Ducati 999R', 'Yamaha R7']
DB = 'test_db.db'


class WetRunOrCommaFuckTheMan(unittest.TestCase):
    """
    Actually make network calls lol.  Thanks, Mr. Newmark!
    This isn't as much of a unittest as an integration test.

    Wrote this while finishing an excellent braggot (Mead and beer's delicious love-child)
    and I'm leaving it the way it is.


    cred.txt is a 3 line text file containing the sending address, password and
    recipient address.  No secrets in code!.
    """

    def setUp(self) -> None:
        with open('tests/cred.txt') as file:
            sender, pw, recipient = file.read().split('\n')
        with Database(DB) as db:
            db.create_database()
            db.set_credentials(sender, pw, recipient)
        with Run(DB) as run:
            for make in MAKES:
                run.city = 'denver'
                run.seller_type = 'both'
                run.vehicle_type = 'motorcycle'
                run.make_model = f'auto_make_model={make.replace(" ", "+")}'
                run.do_add_search()

    def tearDown(self) -> None:
        os.remove(DB)

    def test_threaded_run(self) -> None:
        """
        Test command.Run using threaded option.  I wanted to see performance difference
        vs non-concurrent approach. Turns out that the threaded approach is faster.

        :return: None
        """
        start = time()
        with Run(DB) as run:
            run.do_run_search()
        print(f'Threaded test: {time()-start}.')


if __name__ == '__main__':
    unittest.main()
