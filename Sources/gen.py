import requests
import sys

s = requests.Session()

for username in sys.argv[1:]:
	username = username.strip()
	if username == "":
		continue
	
	# Try to determine the first page that is blank
	
	is_error = False
	
	def presence(page):
		global username
		global is_error
		r = s.get("https://cohost.org/api/v1/trpc/posts.profilePosts?batch=1&input=%7B%220%22%3A%7B%22projectHandle%22%3A%22" + username + "%22%2C%22page%22%3A" + str(page) + '%2C%22options%22%3A%7B%22pinnedPostsAtTop%22%3Atrue%2C%22hideReplies%22%3Afalse%2C%22hideShares%22%3Afalse%2C%22hideAsks%22%3Afalse%2C%22viewingOnProjectPage%22%3Atrue%7D%7D%7D')
#		print(len(r.json()[0]["result"]["data"]["posts"]), "at", page)
		if r.status_code in {404, 500, 400}:
			is_error = True
			return False
		if len(r.json()[0]["result"]["data"]["posts"]) > 0:
			pp_username = r.json()[0]["result"]["data"]["posts"][0]["postingProject"]["handle"]
			assert(username.lower() == pp_username.lower())
			username = pp_username
			return True
		else:
			return False

	lower = 1
	for upper in ([2**x for x in range(1000)]):
		if not presence(upper):
			break
		lower = upper + 1

	while lower != upper:
		mid = (lower + upper) // 2
		if presence(mid):
			lower = mid + 1
		else:
			upper = mid

	if not (is_error and upper == 1):
		for i in range(1, upper + 1):
			print(f"user:{username}+{i}")
