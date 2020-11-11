# python3

class WorkerQueue:
    def __init__(self, numWorkers):
        self.worker_heap = [None] * numWorkers

        for i in range(numWorkers):
            self.worker_heap[i] = Worker(i)
        
        # for i in range((numWorkers // 2) - 1, -1, -1):
        #     self.siftDown(i)

    def GetNextAvailableWorkerForJob(self, jobLength):
        nextAvailable = self.worker_heap[0]
        self.changePriority(0, nextAvailable.time_available + jobLength)
        # self.ShowHeap()
        # print("")
        return nextAvailable

    def changePriority(self, i, p):
        # p_old = self.worker_heap[i].time_available
        # self.worker_heap[i].time_available = p
        # if p > p_old:
        #     self.siftUp(i)
        # else:
        #     self.siftDown(i)
        
        self.siftDown(i)

    def siftUp(self, i):
        while i > 0 and self.compareWorker(i, (i-1)//2):
            self.worker_heap[(i-1)//2], self.worker_heap[i] = self.worker_heap[i], self.worker_heap[(i-1)//2]
            i = (i-1)//2

    def siftDown(self, i):
        n = len(self.worker_heap)
        min_index = i
        l = (2 * i) + 1
        r = (2 * i) + 2
        # print(i,l,r)
        if l < n and self.compareWorker(l, min_index):
            min_index = l
        if r < n and self.compareWorker(r, min_index):
            min_index = r
        if min_index != i:
            self.worker_heap[i], self.worker_heap[min_index] = self.worker_heap[min_index], self.worker_heap[i]
            self.siftDown(min_index)
    
    def compareWorker(self, worker1Index, worker2Index):
        worker1 = self.worker_heap[worker1Index]
        worker2 = self.worker_heap[worker2Index]
        # print(worker1, worker2)
        if worker1.time_available != worker2.time_available:
            return worker1.time_available < worker2.time_available
        else:
            return worker1.id < worker2.id

    def ShowHeap(self):
        for worker in self.worker_heap:
            print("workerID: "+ str(worker.id) + "nextAvailable: " + str(worker.time_available))


class Worker:
    def __init__(self, id):
        self.id = id
        self.time_available = 0
    
class JobRecord:
    def __init__(self, workerId, started_at):
        self.worker = workerId
        self.started_at = started_at



def assign_jobs(n_workers, jobs):
    # TODO: replace this code with a faster algorithm.
    result = []
    workers = WorkerQueue(n_workers)
    # print("HEAP AT BEGINNING")
    # workers.ShowHeap()
    # print("")
    
    for jobSecs in jobs:
        # get the info of the next available worker
        next_worker = workers.GetNextAvailableWorkerForJob(jobSecs)
        # convert that into a job record
        record = JobRecord(next_worker.id, next_worker.time_available - jobSecs)
        # add it to list of job records
        result.append(record)

    return result


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()






