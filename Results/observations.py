import pickle
import pandas as pd

for acc in [0.90, 0.91, 0.92, 0.93]:

	for type in ["","_hybrid"]:
		for n_agents in range(1,4):
			filename = "results_"+str(n_agents)+str(type)+".pkl"
			with open(filename, "rb") as f:
				train_loss, train_acc, test_acc, test_loss, clients, agents, times = pickle.load(f)

			print(filename)

			timet = []
			avg = []
			for i in range(len(test_acc)):
				sum = 0.0
				if i+19 < len(test_acc):
					for j in range(20):
						sum = sum + test_acc[i+j]
					if times[i] > 290000.0:
						break
					avg.append(sum/20.0)
					timet.append(times[i])
					i=i+20

			for i in range(len(avg)):
				if avg[i] >= acc:
					print(str(acc)+", "+str(timet[i])+", "+str(float(i)/float(n_agents)))
					break



	#print("Centralized")
#
	#avg = pd.read_csv("cen_0.2_test_accuracy.csv", header = None)
	#timet = pd.read_csv("cen_0.2_times.csv", header = None)
	#for i in range(len(avg)):
		#if avg[0][i] >= acc:
			#print(str(acc)+", "+str(timet[0][i])+", "+str(i))
			#break



	for topology in ["MESH", "RING", "STAR"]:
		for type in ["","_hybrid","_dynamic","_hybrid_dynamic"]:
			for n_agents in [3]:
				filename = "results_"+topology+"_"+str(n_agents)+type+".pkl"
				with open(filename, "rb") as f:
					train_loss, train_acc, test_acc, test_loss, clients, agents, times = pickle.load(f)

				print(filename)

				timet = []
				avg = []
				for i in range(len(test_acc)):
					sum = 0.0
					if i+19 < len(test_acc):
						for j in range(20):
							sum = sum + test_acc[i+j]
						if times[i] > 290000.0:
							break
						avg.append(sum/20.0)
						timet.append(times[i])
						i=i+20

				for i in range(len(avg)):
					if avg[i] >= acc:
						print(str(acc)+", "+str(timet[i])+", "+str(float(i)/float(n_agents)))
						break

	#with open("results.pkl", "rb") as f:
		#train_loss, train_acc, test_acc, test_loss, clients, agents, times = pickle.load(f)
#
	#print("results.pkl")
#
	#timet = []
	#avg = []
	#for i in range(len(test_acc)):
		#sum = 0.0
		#if i+19 < len(test_acc):
			#for j in range(20):
				#sum = sum + test_acc[i+j]
			#if times[i] > 290000.0:
				#break
			#avg.append(sum/20.0)
			#timet.append(times[i])
			#i=i+20
#
	#for i in range(len(avg)):
		#if avg[i] >= acc:
			#print(str(acc)+", "+str(timet[i])+", "+str(i))
			#break