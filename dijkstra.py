"""
Dino0631
Dijstra network algorthm
"""
import operator
from math import *
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

	@property
	def sorteddiff(self):
		sorted_diff = sorted(self.difficulty.items(), key=operator.itemgetter(1))
		# print('sorteddiff', sorted_diff)
		sortednodes = list(map(lambda x:x[0], sorted_diff))
		return sortednodes


	def connected_to(self,node):
		return self.network == node.network and node.id in self.difficulty

	def __str__(self):
		connections = list(map(lambda x:str(x), list(self.difficulty.keys())))
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

	def add_connection(self, indexes, diff=10):
		"""adds connection of first arg's  with 3rd arg difficulty
		if no difficulty, defaults to 10
		"""
		for index in indexes:
			for i in indexes:
				if i != index:
					self[index].difficulty[i] = diff


	def find_node(self,currentpath:list,destination, pathsexhausted):
		pathlist = []
		# print('current', currentpath)
		# print('dest', destination)
		current = currentpath[-1]
		if destination in self[current].difficulty:
			return currentpath + [destination]
		else:
			for nodenum in self[current].sorteddiff:
				path = currentpath + [nodenum]
				# print(self[nodenum])
				# print('length', len(self[nodenum].difficulty), self[nodenum].difficulty)
				if len(self[nodenum].difficulty) == 1: #if dead end
					# print('continue', nodenum)
					continue
				if nodenum in currentpath: #if already been there
					continue
				bing = self.find_node(path, destination, pathsexhausted)
				# if current in bing:
				# 	return None
				if bing in pathsexhausted:
					continue
				return bing
		return None

	def find_allpaths(self, nodelist:list):
		"""finds shortest path going through all(for now just 2) nodes in list"""
		allpaths = []
		path =  self.find_node([nodelist[0]],nodelist[1], allpaths)
		while path != None:
			allpaths.append(path)
			path =  self.find_node([nodelist[0]],nodelist[1], allpaths)
			# print('penis', path)
			# print('bean', allpaths)
		# print('allpaths:', allpaths)
		return allpaths

	def find_shortest_path(self, nodelist:list):
		"""finds shortest path going through all(for now just 2) nodes in list"""
		allpaths = self.find_allpaths(nodelist)
		shortestpath = allpaths[0]
		for path in allpaths[1:]:
			if self.path_difficulty(shortestpath) > self.path_difficulty(path):
				shortestpath = path
		return shortestpath, self.path_difficulty(shortestpath)


	def path_difficulty(self, nodelist:list):
		full_difficulty = 0
		n = 0
		for node in nodelist[:-1]:
			if nodelist[n+1] not in self[nodelist[n]].difficulty:
				return inf
			full_difficulty += self[nodelist[n]].difficulty[nodelist[n+1]]
			n+=1
		return full_difficulty
		

	def get_node_by_name(self, name:str):
		for i, node in enumerate(self.nodes):
			if node.name == name:
				return i
		return -1

	def add_node(self, name:str, nodedifficulty:dict):
		# print(nodedifficulty)
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
# print(len(roads))
# print(str(roads))
roads2 = Network()
roads2.add_node('P14', {})
roads2.add_node('Q14', {0:10})
roads2 = roads + roads2
roads2.add_node('16thRail', {4:25})
roads2.add_connection([3,6])
roads2.add_connection([1,5])
print('difficulty:', roads2.path_difficulty([0,1,3,4]))
print(roads2)
directions, difficulty = roads2.find_shortest_path([0,7])
print('shortest path:', directions, 'difficulty:', difficulty)
# print(len(roads2))
# print(roads2)
# directions, difficulty = roads2.find_shortest_path([0,7])
# print(directions)
roads3 = Network()
roads3.add_node('key', {})
roads3.add_node('parrot', {})
roads3.add_node('bean2', {0:10})
roads3.add_node('bean', {0:10})
roads3.add_node('cave', {3:10})
roads3.add_node('car', {4:10})
roads3.add_node('bee', {5:10})
roads3.add_node('bar', {6:10, 1:10})
# print(roads3)
# directions = roads3.find_shortest_path([0,1])
# print(directions)
# print(roads+roads2)