from flask import Flask, render_template, request

app = Flask(__name__)

def fcfs(num_processes, burst_times, arrival_times):
    sorted_processes = sorted(zip(arrival_times, burst_times))
    total_time = 0
    turnaround_times = []
    waiting_times = []

    for arrival_time, burst_time in sorted_processes:
        if total_time < arrival_time:
            total_time = arrival_time
        total_time += burst_time
        turnaround_times.append(total_time - arrival_time)
        waiting_times.append(total_time - arrival_time - burst_time)

    average_turnaround_time = round(sum(turnaround_times) / num_processes, 2)
    average_waiting_time = round(sum(waiting_times) / num_processes, 2)

    return average_turnaround_time, average_waiting_time

def sjf(num_processes, burst_times, arrival_times):
    remaining_times = burst_times.copy()
    completion_times = [0] * num_processes
    turnaround_times = [0] * num_processes
    waiting_times = [0] * num_processes

    current_time = 0
    completed_processes = 0
    process_sequence = []

    while completed_processes < num_processes:
        shortest_index = -1
        shortest_burst = float('inf')

        for i in range(num_processes):
            if arrival_times[i] <= current_time and remaining_times[i] < shortest_burst and remaining_times[i] > 0:
                shortest_burst = remaining_times[i]
                shortest_index = i

        if shortest_index == -1:
            current_time += 1
            continue

        current_time += remaining_times[shortest_index]
        completion_times[shortest_index] = current_time
        turnaround_times[shortest_index] = completion_times[shortest_index] - arrival_times[shortest_index]
        waiting_times[shortest_index] = turnaround_times[shortest_index] - burst_times[shortest_index]
        remaining_times[shortest_index] = 0
        completed_processes += 1
        process_sequence.append(shortest_index)

    average_turnaround_time = round(sum(turnaround_times) / num_processes, 2)
    average_waiting_time = round(sum(waiting_times) / num_processes, 2)

    return average_turnaround_time, average_waiting_time

def strf(num_processes, burst_times, arrival_times):
    turnaround_times = []
    waiting_times = []
    completion_times = []

    current_time = 0
    remaining_times = burst_times.copy()
    completed_processes = 0

    while completed_processes < num_processes:
        shortest_remaining_time = float('inf')
        shortest_index = -1

        for i in range(num_processes):
            if arrival_times[i] <= current_time and remaining_times[i] < shortest_remaining_time and remaining_times[i] > 0:
                shortest_remaining_time = remaining_times[i]
                shortest_index = i

        if shortest_index == -1:
            current_time += 1
            continue

        remaining_times[shortest_index] -= 1

        if remaining_times[shortest_index] == 0:
            completed_processes += 1
            finish_time = current_time + 1
            turnaround_time = finish_time - arrival_times[shortest_index]
            waiting_time = turnaround_time - burst_times[shortest_index]
            turnaround_times.append(turnaround_time)
            waiting_times.append(waiting_time)
            completion_times.append(finish_time)

        current_time += 1

    average_turnaround_time = round(sum(turnaround_times) / num_processes, 2)
    average_waiting_time = round(sum(waiting_times) / num_processes, 2)

    return average_turnaround_time, average_waiting_time

def round_robin(num_processes, burst_times, arrival_times, time_quantum):
    waiting_times = [0] * num_processes
    remaining_times = burst_times.copy()
    current_time = 0
    arrival_queue = sorted(zip(arrival_times, burst_times))
    arrival_times_sorted = [x[0] for x in arrival_queue]
    burst_times_sorted = [x[1] for x in arrival_queue]

    while True:
        done = True
        for i in range(num_processes):
            if remaining_times[i] > 0:
                done = False
                if arrival_times_sorted[i] <= current_time:
                    if remaining_times[i] > time_quantum:
                        current_time += time_quantum
                        remaining_times[i] -= time_quantum
                    else:
                        current_time += remaining_times[i]
                        waiting_times[i] = current_time - burst_times_sorted[i] - arrival_times_sorted[i]
                        remaining_times[i] = 0
                else:
                    current_time = arrival_times_sorted[i]
        if done:
            break

    turnaround_times = [burst_times_sorted[i] + waiting_times[i] for i in range(num_processes)]
    average_turnaround_time = round(sum(turnaround_times) / num_processes, 2)
    average_waiting_time = round(sum(waiting_times) / num_processes, 2)

    return average_turnaround_time, average_waiting_time

def priority_non_preemptive(num_processes, burst_times, arrival_times, priorities):
    remaining_times = burst_times.copy()
    completion_times = [0] * num_processes
    turnaround_times = [0] * num_processes
    waiting_times = [0] * num_processes

    current_time = 0
    completed_processes = 0
    process_sequence = []

    while completed_processes < num_processes:
        highest_priority_index = -1
        highest_priority = float('inf')

        for i in range(num_processes):
            if arrival_times[i] <= current_time and priorities[i] < highest_priority and remaining_times[i] > 0:
                highest_priority = priorities[i]
                highest_priority_index = i

        if highest_priority_index == -1:
            current_time += 1
            continue

        current_time += remaining_times[highest_priority_index]
        completion_times[highest_priority_index] = current_time
        turnaround_times[highest_priority_index] = completion_times[highest_priority_index] - arrival_times[highest_priority_index]
        waiting_times[highest_priority_index] = turnaround_times[highest_priority_index] - burst_times[highest_priority_index]
        remaining_times[highest_priority_index] = 0
        completed_processes += 1
        process_sequence.append(highest_priority_index)

    average_turnaround_time = round(sum(turnaround_times) / num_processes, 2)
    average_waiting_time = round(sum(waiting_times) / num_processes, 2)

    return average_turnaround_time, average_waiting_time

def priority_preemptive(num_processes, burst_times, arrival_times, priorities):
    turnaround_times = []
    waiting_times = []
    completion_times = []

    current_time = 0
    remaining_times = burst_times.copy()
    completed_processes = 0

    while completed_processes < num_processes:
        highest_priority = float('inf')
        highest_priority_index = -1

        for i in range(num_processes):
            if arrival_times[i] <= current_time and priorities[i] < highest_priority and remaining_times[i] > 0:
                highest_priority = priorities[i]
                highest_priority_index = i

        if highest_priority_index == -1:
            current_time += 1
            continue

        remaining_times[highest_priority_index] -= 1

        if remaining_times[highest_priority_index] == 0:
            completed_processes += 1
            finish_time = current_time + 1
            turnaround_time = finish_time - arrival_times[highest_priority_index]
            waiting_time = turnaround_time - burst_times[highest_priority_index]
            turnaround_times.append(turnaround_time)
            waiting_times.append(waiting_time)
            completion_times.append(finish_time)

        current_time += 1

    average_turnaround_time = round(sum(turnaround_times) / num_processes, 2)
    average_waiting_time = round(sum(waiting_times) / num_processes, 2)

    return average_turnaround_time, average_waiting_time

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            algorithm = request.form['algorithm']
            num_processes = int(request.form['num_processes'])
            burst_times = [int(request.form[f'burst_time_{i+1}']) for i in range(num_processes)]
            arrival_times = [int(request.form[f'arrival_time_{i+1}']) for i in range(num_processes)]
            time_quantum = int(request.form['time_quantum']) if 'time_quantum' in request.form and request.form['time_quantum'].isdigit() else None
            priorities = [int(request.form[f'priority_{i+1}']) for i in range(num_processes)] if 'priority_1' in request.form else None

            if algorithm == 'fcfs':
                avg_turnaround, avg_waiting = fcfs(num_processes, burst_times, arrival_times)
            elif algorithm == 'sjf':
                avg_turnaround, avg_waiting = sjf(num_processes, burst_times, arrival_times)
            elif algorithm == 'strf':
                avg_turnaround, avg_waiting = strf(num_processes, burst_times, arrival_times)
            elif algorithm == 'round_robin':
                avg_turnaround, avg_waiting = round_robin(num_processes, burst_times, arrival_times, time_quantum)
            elif algorithm == 'priority_non_preemptive':
                avg_turnaround, avg_waiting = priority_non_preemptive(num_processes, burst_times, arrival_times, priorities)
            elif algorithm == 'priority_preemptive':
                avg_turnaround, avg_waiting = priority_preemptive(num_processes, burst_times, arrival_times, priorities)
            
            results = {
                'average_turnaround_time': avg_turnaround,
                'average_waiting_time': avg_waiting
            }
            return render_template('index.html', results=results)
        except ValueError as e:
            error = f"Error: {str(e)}"
            return render_template('index.html', error=error)

    return render_template('index.html')

if __name__ == "__main__": app.run(debug=True):
    app.run(debug=True)
