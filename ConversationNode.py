"""
This module provides a ConversationNode class to represent a node in a conversation tree.
Each node stores the user who sent the message and the text of the message.
Nodes can have children, which represent replies or follow-up messages.

Features:
- Add child nodes to simulate a conversation.
- Print the conversation from any node to the root.
- Serialize the conversation tree to a JSON file.
- Deserialize a conversation tree from a JSON file.

Tutorial:
1. Create a root node:
	root = ConversationNode(user="ROBOT", text="Hey, who is this?")

2. Add child nodes:
	resp1 = ConversationNode("Enrique", "EM")
	root.add(resp1)

3. Navigate through the conversation:
	curr = resp1

4. Save the conversation to a file:
	root.save_conversation_tree(curr=curr)

5. Load the conversation from a file:
	root, curr = ConversationNode.load_conversation_tree()
"""

import json

class ConversationNode:
	"""
	Represents a node in a conversation tree.

	Attributes:
		user (str): The user who sent the message.
		text (str): The text of the message.
		depth (int): The depth of the node in the tree.
		parent (ConversationNode): The parent node.
		children (list): The child nodes.
	"""
	def __init__(self, text="None", user="N/A"):
		"""
		Initializes a ConversationNode with text and user.

		Parameters:
			text (str): The text of the message. Defaults to "None".
			user (str): The user who sent the message. Defaults to "N/A".
		"""
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
		"""
		Adds a child node to the current node.

		Parameters:
			msg (ConversationNode): The child node to add.
		"""
		assert isinstance(msg, ConversationNode)
		self.children.append(msg)
		msg.depth = self.depth + 1
		msg.parent = self

	def print_conversation(self):
		"""
		Prints the conversation from the current node to the root node.
		"""
		if self.parent:
			self.parent.print_conversation()
		print(f"{self.user}: {self.text}")

	def return_conversation(self):
		"""
		Returns the conversation from the current node to the root node.
		"""

		if self.parent:
			conv = self.parent.return_conversation()
		else:
			conv = []

		return conv + [(self.user, self.text)]

	def save_conversation_tree(self, filename="test.conv", curr=None):
		"""
        Saves the conversation tree to a file.

        Parameters:
            filename (str): The name of the file to save the tree to. Defaults to "test.conv".
            curr (ConversationNode): The current node in the conversation. Defaults to None.
        """
		data = self.serialize()
		curr_path = self.find_path_to_node(curr)
		with open(filename, 'w') as file:
			json.dump({"tree": data, "curr_path": curr_path}, file, indent=4)

	@staticmethod
	def load_conversation_tree(filename="test.conv"):
		"""
        Loads the conversation tree from a file.

        Parameters:
            filename (str): The name of the file to load the tree from. Defaults to "test.conv".

        Returns:
            tuple: The root and current nodes (root, curr).
        """
		with open(filename, 'r') as file:
			data = json.load(file)
			root = ConversationNode.deserialize(data["tree"])
			curr = root.find_node_by_path(data["curr_path"])
			return root, curr

	def serialize(self):
		"""
        Serializes the node to a dictionary.

        Returns:
            dict: A dictionary representation of the node.
        """
		children_data = [child.serialize() for child in self.children]
		return {
			"user": self.user,
			"text": self.text,
			"depth": self.depth,
			"children": children_data
		}

	@staticmethod
	def deserialize(data):
		"""
        Deserializes a node from a dictionary.

        Parameters:
            data (dict): The dictionary containing the serialized node data.

        Returns:
            ConversationNode: The deserialized node.
        """
		node = ConversationNode(data["text"], data["user"])
		node.depth = data["depth"]
		for child_data in data["children"]:
			child = ConversationNode.deserialize(child_data)
			node.add(child)
		return node

	def find_path_to_node(self, node, path=None):
		"""
        Finds the path to a node in the tree.

        Parameters:
            node (ConversationNode): The node to find the path to.
            path (list): The current path. Should not be specified by the user.

        Returns:
            list: The path to the node as a list of child indices.
        """
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
		"""
        Finds a node by its path in the tree.

        Parameters:
            path (list): The path to the node as a list of child indices.

        Returns:
            ConversationNode: The node at the specified path.
        """
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

	print(resp21.return_conversation())
	for _ in range(3):  # Reduced to 1 iteration for demonstration
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

