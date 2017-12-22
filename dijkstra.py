"""
Dino0631
Dijstra network algorthm
"""
import math
from copy import deepcopy
class Node():
	"""docstring for Node"""
	nextid = 0 #next id to give node
	def __init__(self, netid:int, nodeid:int, name:str, nodedifficulty:dict):
		# super(Node, self).__init__()
		self.network = netid
		self.name = name
		self.difficulty = nodedifficulty #difficulty 
		#to go from current node to node in dict
		self.id = nodeid# Node.nextid
		Node.nextid += 1

	def connected_to(node):
		return self.network == node.network and node.id in self.difficulty

	def __str__(self):
		connections = list(map(lambda x:str(x), list(node.difficulty.keys())))
		return 'net[{}] [{}] {}, connections: {}'.format(
			self.network, self.id, self.name,', '.join(connections))

class Network:
	"""Network of Nodes"""
	nextid = 0 #next id to give node
	def __init__(self, arg=0):
		self.nodes = []
		if arg != None:
			self.id = Network.nextid
			Network.nextid += 1
		else:
			self.id=None
	
	@classmethod
	def is_net(self, obj):
		return type(obj) == type(Network())

	@property
	def lastnode(self):
		if len(self) == 0:
			return None
		return self.nodes[len(self)-1]

	def add_connection(self, connect:list):
		"""adds connection of first 2 elements with 3rd element difficulty
		if no difficulty, defaults to 10
		"""
		#todo
		pass
		
	def find_shortest_path(self, nodelist:list):
		"""finds shortest path going through all nodes in list"""
		#todo implement it
		pass

	def get_node_by_name(self, name:str):
		for i, node in enumerate(self.nodes):
			if node.name == name:
				return i
		return -1

	def add_node(self, name:str, nodedifficulty:dict):
		print(nodedifficulty)
		nextid = len(self)
		# print('nextid:', nextid)
		for nodeindex in nodedifficulty:
			# print(len(self.nodes))
			# print(nodeindex, Node.nextid)
			if nodeindex < len(self):
				self.nodes[nodeindex].difficulty[nextid] = nodedifficulty[nodeindex]
		self.nodes.append(Node(self.id,nextid,name,nodedifficulty))

	def __len__(self):
		return len(self.nodes)

	def __gt__(self, othernet):
		"""determines if self has more nodes"""
		if not Network.is_net(othernet):
			return None
		return len(self)>len(othernet)

	def __lt__(self, othernet):
		"""determines if self has less nodes"""
		if not Network.is_net(othernet):
			return None
		return len(self)>len(othernet)


	def __eq__(self, othernet):
		"""determines if self has exact same nodes as othernet"""
		if not Network.is_net(othernet):
			return None
		if len(self) != len(othernet):
			return False
		for i in range(len(self)):
			if self.nodes[i] != othernet.nodes[i]:
				return False
		return True

	def __str__(self):
		"""shows list of nodes and their connections"""
		displaylist = []
		for node in self.nodes:
			connections = list(map(lambda x:str(x), list(node.difficulty.keys())))
			displaylist.append('[{}] {}, connections: {}'.format(
				node.id, node.name, ', '.join(connections)))
		return '\n'.join(displaylist)

	def __contains__(self, value:str):
		"""Checks if Network has node with name 'value'"""
		for node in self.nodes:
			if node.name == value:
				return True
		return False

	def __getitem__(self, index):
		"""gets index-th node in network"""
		return self.nodes[index]

	def __add__(self, othernet):
		"""sums up all nodes of both networks"""
		if not Network.is_net(othernet):
			return None
		returnnet = Network(None)
		# print('lenofself:', len(self))
		# print('returnnet:', returnnet)
		for node in self:
			returnnet.add_node(node.name, node.difficulty)
		# print(returnnet)
		for i, node in enumerate(othernet):
			# print(returnnet)
			# print(node.difficulty)
			nodedifficulty = deepcopy(node.difficulty)
			for nodeid in nodedifficulty:
				diff = node.difficulty.pop(nodeid, None)
				# print('thing', len(self)+nodeid)
				# print(len(self), nodeid)
				node.difficulty[len(self)+nodeid] = diff
			returnnet.add_node(node.name, node.difficulty)

		return returnnet


roads = Network()
roads.add_node('P12', {})
roads.add_node('P13', {0:10})
roads.add_node('Q12', {0:10})
roads.add_node('Q13', {1:10,2:10})
roads.add_node('13thRail', {2:2, 3:2})
print(len(roads))
print(str(roads))
roads2 = Network()
roads2.add_node('P14', {})
roads2.add_node('Q14', {0:10})
print(len(roads2))
print(roads2)
print(roads+roads2)