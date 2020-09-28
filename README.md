# Overtime
> A temporal networks library written in [Python](https://www.python.org/).


## Simple Example
```python
import overtime as ot

network = ot.TemporalDiGraph('Sample Network', data=ot.CsvInput('./data/network.csv'))
network.add_node('g')
network.add_edge('f', 'h', 3)
network.details()

>>>	Graph Details: 
	Label: SampleNetwork 
	Directed: True 
	Static: False
	#Nodes: 7 
	#Edges: 15

ot.Circle(network)
ot.calculate_reachability(network, 'b')
>>> 5
```



## Extended Example
> See [tfl_example.py](https://github.com/soca-git/COMP702-Temporal-Networks-Library/blob/master/tfl_example.py).


## Install

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install overtime.

```bash
pip install overtime
```


## License

[MIT](https://choosealicense.com/licenses/mit/)
