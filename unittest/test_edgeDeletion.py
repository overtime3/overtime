import unittest
import overtime as ot


class TestEdgeDeletion(unittest.TestCase):
    '''
    This class is used to test the two main edge deletion method in edgeDeletion.py.

    '''
    def setUp(self) -> None:
        '''
        Load two networks. The first one is a simple test network, and the second one is the London subway
        stations network(Victoria).

        '''

        # load data (simple network)
        self.network1 = ot.TemporalDiGraph('test_network', data=ot.CsvInput('../overtime/data/network.csv'))

        # load data (London subway stations - Victoria)
        tfl_data = ot.CsvInput('../overtime/data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv')
        self.network2 = ot.TemporalDiGraph('TflNetwork', data=tfl_data)
        self.network2.nodes.add_data('../overtime/data/victoria_central_bakerloo_piccadilly-stations.csv')

    def test_h_approximation(self):
        '''
        This function is used to test h_approximation algorithm.
        Firstly, it will specify h and flag (default value is True), respectively.
        And then, it will run the h_approximation algorithm on two networks.
        Finally, it will check the temporal reachaility of the network after running the h_approximation algorithm.
        If there is some node whose temporal reachability is more than h, then the flag will change to False and the
        test case will not pass.

        '''
        h1 = 3
        flag1 = True
        ot.h_approximation(self.network1, h1)

        # check if all the temporal reachability of network1 is less than h1
        for node in self.network1.nodes.set:
            reachability = ot.calculate_reachability(self.network1, node.label)
            if reachability > h1:
                flag1 = False
                break

        self.assertTrue(flag1)

        h2 = 100
        flag2 = True
        ot.h_approximation(self.network2, h2)
        # check if all the temporal reachability of network2 is less than h2
        for node in self.network2.nodes.set:
            reachability = ot.calculate_reachability(self.network2, node.label)
            if reachability > h2:
                flag2 = False
                break
        self.assertTrue(flag2)

    def test_c_approximation(self):
        '''
        This function is used to test c_approximation algorithm.
        Firstly, it will specify h and flag (default value is True), respectively.
        And then, it will run the c_approximation algorithm on two networks.
        Finally, it will check the temporal reachaility of the network after running the c_approximation algorithm.
        If there is some node whose temporal reachability is more than h, then the flag will change to False and the
        test case will not pass.

        '''
        h1 = 3
        flag1 = True
        ot.c_approximation(self.network1, h1, ot.generate_Layout(self.network1))

        # check if all the temporal reachability of network1 is less than h1
        for node in self.network1.nodes.set:
            reachability = ot.calculate_reachability(self.network1, node.label)
            if reachability > h1:
                flag1 = False
                break

        self.assertTrue(flag1)

        h2 = 100
        flag2 = True
        ot.c_approximation(self.network2, h2, ot.generate_Layout(self.network2))
        # check if all the temporal reachability of network2 is less than h2
        for node in self.network2.nodes.set:
            reachability = ot.calculate_reachability(self.network2, node.label)
            if reachability > h2:
                flag2 = False
                break
        self.assertTrue(flag2)


if __name__ == '__main__':
    unittest.main()


