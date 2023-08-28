'''
The executable for the CLI interface.
'''
from ConversationNode import ConversationNode

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