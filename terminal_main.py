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

	def save_conversation_tree(self, filename="test.conv"):
		data = self.serialize()
		with open(filename, 'w') as file:
			json.dump(data, file, indent="4")

	@staticmethod
	def load_conversation_tree(self, filename="test.conv"):
		with open(filename, 'r') as file:
			data = json.load(file)
			return ConversationNode.deserialize(data)

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

def test_conversation_print():
	root = ConversationNode(user="Terminal", text="Hey, type a message.")
	mid = ConversationNode("test1")
	curr = ConversationNode("test2")
	root.add(mid)
	mid.add(curr)
	
	curr.print_conversation()

def main():
	root = ConversationNode(user="Terminal", text="Hey, type a message.")
	root.print_conversation()
	curr = root
	i = 0
	while True:
		user_input = input("#BR,BK,MW,S,L>")
		if user_input == "#BR":
			break
		elif user_input == "#BK":
			if curr.parent:
				curr = curr.parent
			if curr.parent:
				curr = curr.parent
		elif user_input == "#MW":
			print(root)
		elif user_input == "#S":
			root.save_conversation_tree()
		elif user_input == "#L":
			root = ConversationNode.load_conversation_tree()
			curr = root
		else:
			ncurr = ConversationNode(user_input, f"User {i%2 + 1}")
			i += 1
			curr.add(ncurr)
			curr = ncurr
		curr.print_conversation()

if __name__ == "__main__":
	main()