import csv
import numpy as np
import matplotlib.pyplot as plt

def main():
    iFile = open('result.csv', 'rb')
    reader = csv.reader(filter(lambda row: row[0]!='#', iFile))

    values = {}
    average = {}
    points_A_vector = []
    points_B_vector = []
    diff_vector = []

    # read values from csv file
    for row in reader:
        points_A_vector.append(int(row[3]))
        points_B_vector.append(int(row[4]))
        diff_vector.append(int(row[5]))
        # group by frame_skip_A, frame_skip_B
        if values.has_key((int(row[0]),int(row[1]))):
            scoreA = values.get((int(row[0]),int(row[1])))[0]
            scoreB = values.get((int(row[0]),int(row[1])))[1]
            reward = values.get((int(row[0]),int(row[1])))[2]
            scoreA.append(int(row[3]))
            scoreB.append(int(row[4]))
            reward.append(int(row[5]))
            values[(int(row[0]), int(row[1]))] = (scoreA, scoreB, reward)
        else:
            values[(int(row[0]),int(row[1]))] = ([int(row[3])],[int(row[4])],[int(row[5])])

    # calculate average score_A, score_B and reward
    for it in values:
        avg_scoreA = sum(values.get(it)[0]) / float(len(values.get(it)[0]))
        avg_scoreB = sum(values.get(it)[1]) / float(len(values.get(it)[1]))
        avg_reward = sum(values.get(it)[2]) / float(len(values.get(it)[2]))
        average[it] = (avg_scoreA, avg_scoreB, avg_reward)

    # write average back to file
    result_file = open("average.csv", "w")
    result_file.write("# frame_skip_agent_A, frame_skip_agent_B, avg_score_A, avg_score_B, avg_difference\n")
    for it in average:
        result_file.write("%s,%s,%.2f,%.2f,%.2f\n" % (it[0], it[1], average.get(it)[0], average.get(it)[1], average.get(it)[2]))
    result_file.close()
    iFile.close()

    # extract the plot data and plot graphs
    for fixed_frame_skip in range(1,31,1):
        frame_skip_opponent = np.arange(1, 31, 1)
        average_difference_A = []
        average_difference_B = []
        for i in frame_skip_opponent:
            average_difference_A.append(average.get((fixed_frame_skip,i))[2])
            average_difference_B.append(-average.get((i,fixed_frame_skip))[2])
        plot_frame_skip(frame_skip_opponent, average_difference_A, average_difference_B, fixed_frame_skip)

    # calculate and output the total scores and relate the total difference in % to the total of all points scored
    stat_file = open("statistics.txt", "w")
    stat_file.write("total sessions: %d\n" % (len(points_A_vector)))
    stat_file.write("total points A: %d\n" %(sum(points_A_vector)))
    stat_file.write("total points B: %d\n" % (sum(points_B_vector)))
    stat_file.write("total difference: %d\n" % (sum(diff_vector)))
    stat_file.write("average difference per session: %.4f\n" % (sum(diff_vector)/float(len(points_A_vector))))
    stat_file.write("total difference in %% from total points: %.4f\n" % (float(100)*sum(diff_vector)/(sum(points_A_vector)+sum(points_B_vector))))
    stat_file.close()

# plot average difference / frame skip opponent graphs with fixed frame skip of frame_skip
def plot_frame_skip(frame_skip_opponent, average_difference_A, average_difference_B, fixed_frame_skip):
    plt.plot(frame_skip_opponent, average_difference_A, 'ro', label='Player A')
    plt.plot(frame_skip_opponent, average_difference_B, 'bs', label='Player B')

    legend = plt.legend(loc='upper left', shadow=True)
    plt.xlabel('frame skip opponent (frames)')
    plt.ylabel('average result difference (points)')
    plt.title('Fixed frame skip of %s' %(fixed_frame_skip))
    plt.grid(True)

    plt.savefig("plots/frame_skip_%s.png" %(fixed_frame_skip))
    plt.close()

# execute the program
main()
