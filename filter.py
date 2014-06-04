import math
import os

def words(filename):
	# Get list of lines
	infile = open(filename,'r')
	lines = infile.readlines()
	infile.close()

	# For each line, delimit word by space 
	# and add to list of words. Also, convert
	# all words to lowercase for convenience
	return [word.strip().lower() for line in lines for word in line.split()]

def lexicon(k):
	# Extract training directories
	spam_training_directory = os.getcwd() + '/emails/spamtraining'
	ham_training_directory  = os.getcwd() + '/emails/hamtraining'

	# Create spam distribution
	spam_distribution = {}
	files = os.listdir(spam_training_directory)
	for file in files:
		list_of_words = words(spam_training_directory + '/' + file)
		for word in list_of_words:
			if word in spam_distribution:
				spam_distribution[word] += 1
			else:
				spam_distribution[word] = 1

	# Create ham distribution
	ham_distribution = {}
	files = os.listdir(ham_training_directory)
	for file in files:
		list_of_words = words(ham_training_directory + '/' + file)
		for word in list_of_words:
			if word in ham_distribution:
				ham_distribution[word] += 1
			else:
				ham_distribution[word] = 1

	# Remove all key,value pairs that
	# have a value less than k
	hamkeys  = ham_distribution.keys()
	spamkeys = spam_distribution.keys()

	for key in spamkeys:
		if spam_distribution[key] < k:
			del spam_distribution[key]

	for key in hamkeys:
		if ham_distribution[key] < k:
			del ham_distribution[key]

	return ham_distribution, spam_distribution

def probability(word, category, ham_distribution, spam_distribution, m):
	# Compute P(w = word | category), smoothing the result
	# with Laplacian Smoothing with parameter m

	distribution = ham_distribution if category == 'ham' else spam_distribution

	V = len(distribution)

	keys = distribution.keys()

	numerator = (distribution[word] + m if word in keys else m)
	denominator = sum([distribution[key] for key in keys]) + m*V

	return numerator / float(denominator)

def classify_email(email, ham_distribution, spam_distribution, m):
	email_words = words(email)

	ham_probability  = 0
	spam_probability = 0

	for word in email_words:
		ham_probability  += math.log(probability(word, 'ham', ham_distribution, spam_distribution, m))
		spam_probability += math.log(probability(word, 'spam', ham_distribution, spam_distribution, m))

	return 'ham' if ham_probability > spam_probability else 'spam'

def test_filter(hamtesting, spamtesting, k, m):
	ham_distribution, spam_distribution = lexicon(k)

	spam_as_ham = []
	ham_as_spam = []

	ham_hit   = 0
	ham_total = 0
	ham_testing_files = os.listdir(hamtesting)
	for file in ham_testing_files:
		if classify_email(hamtesting + '/' + file, ham_distribution, spam_distribution, m) == 'ham':
			ham_hit += 1
		else:
			ham_as_spam.append(file)
		ham_total += 1

	spam_hit   = 0
	spam_total = 0
	spam_testing_files = os.listdir(spamtesting)
	for file in spam_testing_files:
		if classify_email(spamtesting + '/' + file, ham_distribution, spam_distribution, m) == 'spam':
			spam_hit += 1
		else:
			spam_as_ham.append(file)
		spam_total += 1

	ham_hit_ratio  = ham_hit / float(ham_total)
	spam_hit_ratio = spam_hit / float(spam_total)

	return ham_hit_ratio, spam_hit_ratio, ham_total, spam_total, ham_as_spam, spam_as_ham

# ---------- CODE STARTS HERE ----------

spamtesting = os.getcwd() + '/emails/spamtesting'
hamtesting  = os.getcwd() + '/emails/hamtesting'

ham_hit_ratio, spam_hit_ratio, ham_total, spam_total, ham_as_spam, spam_as_ham = test_filter(hamtesting, spamtesting, k=5, m=1)

print 
print "Correct Ham Percentage:     ", ham_hit_ratio * 100
print "Correct Spam Percentage:    ", spam_hit_ratio * 100
print "Correct Overall Percentage: ", (ham_hit_ratio*ham_total + spam_hit_ratio*spam_total) / (ham_total + spam_total) * 100

print "\nHam Incorrectly Labelled as Spam:"
for file in ham_as_spam:
	print "\t"+file

print "\nSpam Incorrectly Labelled as Ham:"
for file in spam_as_ham:
	print "\t"+file
print