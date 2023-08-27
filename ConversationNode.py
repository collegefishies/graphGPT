import json

class ConversationNode:
	def __init__(self, text = "None", user = "N/A"):
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
		if curr is not None:
			assert isinstance(curr, ConversationNode)

		data = self.serialize(curr=curr)
		with open(filename, 'w') as file:
			json.dump(data, file, indent=4)

	@staticmethod
	def load_conversation_tree(self=None,filename="test.conv"):
		curr = None
		with open(filename, 'r') as file:
			data = json.load(file)
			if "curr" in data:
				curr = data["curr"]
			return ConversationNode.deserialize(data), ConversationNode.deserialize(curr)

	def serialize(self, curr=None):
		children_data = [child.serialize() for child in self.children]
		if curr is None:
			return {
				"user": self.user,
				"text": self.text,
				"depth": self.depth,
				"children": children_data
			}
		else:
			return {
				"curr": curr.serialize(),
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

	curr = resp11

	# try:
	#	root.save_conversation_tree()
	#	print("Saved conversation tree.")
	# except:
	#	print("Failed to save conversation tree.")
	# try:
	#	root, curr = ConversationNode.load_conversation_tree()
	#	print("Loaded conversation tree.")
	# except Exception as e:
	#	print("Failed to load conversation tree.")
	#	print(e)

	for _ in range(5):
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
			print("Loaded conversation tree with position.")
		except Exception as e:
			print("Failed to load conversation tree with position.")
			print(e)



if __name__ == '__main__':
	main()
