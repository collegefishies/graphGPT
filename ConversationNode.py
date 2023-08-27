# Refactored version of the code considering the mentioned issues

import json

class ConversationNode:
	def __init__(self, text="None", user="N/A"):
		self.user = user
		self.text = text
		self.depth = 0
		self.parent = None
		self.children = []

	def __str__(self):
		_str = f"{self.user}:\"{self.text}\""
		if len(self.children) > 0:
			_str += f"\nChildren:[{','.join([str(x) for x in self.children])}]"
		return _str

	def add(self, msg):
		assert isinstance(msg, ConversationNode)
		self.children.append(msg)
		msg.depth = self.depth + 1
		msg.parent = self

	def print_conversation(self):
		if self.parent:
			self.parent.print_conversation()
		print(f"{self.user}: {self.text}")

	def save_conversation_tree(self, filename="test.conv", curr=None):
		data = self.serialize()
		curr_path = self.find_path_to_node(curr)
		with open(filename, 'w') as file:
			json.dump({"tree": data, "curr_path": curr_path}, file, indent=4)

	@staticmethod
	def load_conversation_tree(filename="test.conv"):
		with open(filename, 'r') as file:
			data = json.load(file)
			root = ConversationNode.deserialize(data["tree"])
			curr = root.find_node_by_path(data["curr_path"])
			return root, curr

	def serialize(self):
		children_data = [child.serialize() for child in self.children]
		return {
			"user": self.user,
			"text": self.text,
			"depth": self.depth,
			"children": children_data
		}

	@staticmethod
	def deserialize(data):
		node = ConversationNode(data["text"], data["user"])
		node.depth = data["depth"]
		for child_data in data["children"]:
			child = ConversationNode.deserialize(child_data)
			node.add(child)
		return node

	def find_path_to_node(self, node, path=None):
		if path is None:
			path = []
		if self == node:
			return path
		for i, child in enumerate(self.children):
			new_path = path + [i]
			found_path = child.find_path_to_node(node, new_path)
			if found_path:
				return found_path
		return None

	def find_node_by_path(self, path):
		node = self
		for i in path:
			node = node.children[i]
		return node

def main():
	root = ConversationNode(user="ROBOT", text="Hey, who is this?")
	resp1 = ConversationNode("Enrique", "EM")
	resp2 = ConversationNode("Grace", "GX")
	resp11 = ConversationNode("Nice to meet you, Enrique!", "ROBOT")
	resp21 = ConversationNode("What kind of name is Grace?", "ROBOT")

	root.add(resp1)
	root.add(resp2)
	resp1.add(resp11)
	resp2.add(resp21)

	curr = resp1
	hadparent = curr.parent is not None
	oldparent = curr.parent

	for _ in range(1):  # Reduced to 1 iteration for demonstration
		try:
			root.save_conversation_tree(curr=curr)
			print("Saved conversation tree with position.")
		except Exception as e:
			print("Failed to save conversation tree with position.")
			print(e)

		try:
			root, curr = ConversationNode.load_conversation_tree()
			assert isinstance(root, ConversationNode)
			assert isinstance(curr, ConversationNode)
			if hadparent:
				assert curr.parent is not None
				# assert curr.parent == oldparent
				print(curr.parent)
				print(oldparent)
				print("Loaded conversation tree with position and parent.")
			print("Loaded conversation tree with position.")
		except Exception as e:
			print("Failed to load conversation tree with position.")
			print(e)

if __name__ == '__main__':
	main()

