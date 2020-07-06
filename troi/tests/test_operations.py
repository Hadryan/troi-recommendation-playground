import os
import unittest

from troi import Artist, Release, Recording
import troi.operations 


class TestOperations(unittest.TestCase):

    def test_is_homogeneous(self):
        alist = [ ]
        assert troi.operations.is_homogeneous(alist) == True

        alist = [ Artist(), Artist() ]
        assert troi.operations.is_homogeneous(alist) == True

        alist = [ Artist(), Release() ]
        assert troi.operations.is_homogeneous(alist) == False

    def test_unique(self):
        # Test artists
        alist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']), 
                  Artist(mbids=['a1c35a51-d102-4ce7-aefb-79a361e843b6']) ]
        u_alist = troi.operations.unique(alist, 'mbids')
        assert len(u_alist) == 2

        alist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']), 
                  Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']) ]
        u_alist = troi.operations.unique(alist, 'mbids')
        assert len(u_alist) == 1
        assert u_alist[0].mbids == ['8756f690-18ca-488d-a456-680fdaf234bd']

        alist = [ Artist(artist_credit_id=65),
                  Artist(artist_credit_id=65) ]
        u_alist = troi.operations.unique(alist, 'artist_credit_id')
        assert len(u_alist) == 1
        assert u_alist[0].artist_credit_id == 65

        # Test recording (not testing release since rel and rec use same code)
        rlist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd'), 
                  Recording(mbid='a1c35a51-d102-4ce7-aefb-79a361e843b6') ]
        with self.assertRaises(ValueError):
            u_rlist = troi.operations.unique(rlist, 'mbids')
        u_rlist = troi.operations.unique(rlist, 'mbid')
        assert len(u_rlist) == 2

        rlist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd'), 
                  Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd') ]
        u_rlist = troi.operations.unique(rlist, 'mbid')
        assert len(u_rlist) == 1
        assert u_rlist[0].mbid == '8756f690-18ca-488d-a456-680fdaf234bd'

    def test_ensure_conformity(self):
        # Test artists
        alist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']), 
                  Artist(mbids=['73a9d0db-0ec7-490e-9a85-0525a5ccef8e']) ]
        blist = [ Artist(mbids=['a1c35a51-d102-4ce7-aefb-79a361e843b6']) ]
        assert troi.operations._ensure_conformity(alist, blist) == True

        alist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']), 
                  Artist(mbids=['73a9d0db-0ec7-490e-9a85-0525a5ccef8e']) ]
        blist = [ Release(mbid='a1c35a51-d102-4ce7-aefb-79a361e843b6') ]
        with self.assertRaises(TypeError):
            troi.operations._ensure_conformity(alist, blist)

        # Test recording (not testing release since rel and rec use same code)
        alist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd'), 
                  Recording(mbid='73a9d0db-0ec7-490e-9a85-0525a5ccef8e') ]
        blist = [ Recording(mbid='a1c35a51-d102-4ce7-aefb-79a361e843b6') ]
        assert troi.operations._ensure_conformity(alist, blist) == True

        alist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd'), 
                  Recording(mbid='73a9d0db-0ec7-490e-9a85-0525a5ccef8e') ]
        blist = [ Release(mbid='a1c35a51-d102-4ce7-aefb-79a361e843b6') ]
        with self.assertRaises(TypeError):
            troi.operations._ensure_conformity(alist, blist)

    def test_union(self):
        # Test artists
        alist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']) ]
        blist = [ Artist(mbids=['a1c35a51-d102-4ce7-aefb-79a361e843b6']) ]
        ulist = troi.operations.union(alist, blist)
        assert len(ulist) == 2
        assert ulist[0].mbids == ['8756f690-18ca-488d-a456-680fdaf234bd']
        assert ulist[1].mbids == ['a1c35a51-d102-4ce7-aefb-79a361e843b6']

        # Test recording (not testing release since rel and rec use same code)
        alist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd') ]
        blist = [ Recording(mbid='a1c35a51-d102-4ce7-aefb-79a361e843b6') ]
        ulist = troi.operations.union(alist, blist)
        assert len(ulist) == 2
        assert ulist[0].mbid == '8756f690-18ca-488d-a456-680fdaf234bd'
        assert ulist[1].mbid == 'a1c35a51-d102-4ce7-aefb-79a361e843b6'

    def test_intersection(self):
        # Test artists
        alist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']), 
                  Artist(mbids=['73a9d0db-0ec7-490e-9a85-0525a5ccef8e']) ]
        blist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']) ]
        with self.assertRaises(ValueError):
            ilist = troi.operations.intersection(alist, blist, 'mbid')

        ilist = troi.operations.intersection(alist, blist, 'mbids')
        assert len(ilist) == 1
        assert ilist[0].mbids == blist[0].mbids

        alist = [ Artist(mbids=['73a9d0db-0ec7-490e-9a85-0525a5ccef8e']) ]
        blist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']) ]
        ilist = troi.operations.intersection(alist, blist, 'mbids')
        assert len(ilist) == 0

        # Test recording (not testing release since rel and rec use same code)
        alist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd'), 
                  Recording(mbid='73a9d0db-0ec7-490e-9a85-0525a5ccef8e') ]
        blist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd') ]
        with self.assertRaises(ValueError):
            ilist = troi.operations.intersection(alist, blist, 'mbids')

        ilist = troi.operations.intersection(alist, blist, 'mbid')
        assert len(ilist) == 1
        assert ilist[0].mbid == blist[0].mbid

        alist = [ Recording(mbid='73a9d0db-0ec7-490e-9a85-0525a5ccef8e') ]
        blist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd') ]
        ilist = troi.operations.intersection(alist, blist, 'mbid')
        assert len(ilist) == 0

    def test_difference(self):
        # Test artists
        alist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']), 
                  Artist(mbids=['73a9d0db-0ec7-490e-9a85-0525a5ccef8e']) ]
        blist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']) ]
        with self.assertRaises(ValueError):
            ilist = troi.operations.difference(alist, blist, 'mbid')

        ilist = troi.operations.difference(alist, blist, 'mbids')
        assert len(ilist) == 1
        assert ilist[0].mbids == ['73a9d0db-0ec7-490e-9a85-0525a5ccef8e']

        alist = [ Artist(mbids=['8756f690-18ca-488d-a456-680fdaf234bd']), 
                  Artist(mbids=['73a9d0db-0ec7-490e-9a85-0525a5ccef8e']) ]
        blist = [ Artist(mbids=['a1c35a51-d102-4ce7-aefb-79a361e843b6']) ]
        dlist = troi.operations.difference(alist, blist, 'mbids')
        assert len(dlist) == 2
        assert dlist[0].mbids == ['8756f690-18ca-488d-a456-680fdaf234bd']
        assert dlist[1].mbids == ['73a9d0db-0ec7-490e-9a85-0525a5ccef8e']

        # Test recording (not testing release since rel and rec use same code)
        alist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd'), 
                  Recording(mbid='73a9d0db-0ec7-490e-9a85-0525a5ccef8e') ]
        blist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd') ]
        with self.assertRaises(ValueError):
            ilist = troi.operations.difference(alist, blist, 'mbids')

        ilist = troi.operations.difference(alist, blist, 'mbid')
        assert len(ilist) == 1
        assert ilist[0].mbid == '73a9d0db-0ec7-490e-9a85-0525a5ccef8e'

        alist = [ Recording(mbid='8756f690-18ca-488d-a456-680fdaf234bd'), 
                  Recording(mbid='73a9d0db-0ec7-490e-9a85-0525a5ccef8e') ]
        blist = [ Recording(mbid='a1c35a51-d102-4ce7-aefb-79a361e843b6') ]
        dlist = troi.operations.difference(alist, blist, 'mbid')
        assert len(dlist) == 2
        assert dlist[0].mbid == '8756f690-18ca-488d-a456-680fdaf234bd'
        assert dlist[1].mbid == '73a9d0db-0ec7-490e-9a85-0525a5ccef8e'