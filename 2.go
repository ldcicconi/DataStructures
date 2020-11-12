package main

import (
	"fmt"
	"sync"
	"time"
)

type Worker struct {
	Id        int
	StartTime time.Time
}

func (w *Worker) startWorkingOnJob(jobLength int, returnTo chan Worker, wg *sync.WaitGroup) {
	fmt.Printf("Worker %d starting job for %d\n", w.Id, jobLength)
	time.Sleep(time.Duration(jobLength) * time.Second)
	fmt.Printf("Worker %d done with job\n", w.Id)
	returnTo <- *w
	wg.Done()
	return
}

func main() {
	numWorker := 5
	jobs := []int{5, 3, 6, 1, 6, 2, 3} // [5, 3, 6, 1]

	// generate workers and put them in queue
	workerQueue := make(chan Worker, numWorker)
	for i := 0; i < numWorker; i++ {

		workerQueue <- Worker{
			Id: i,
		}

	}

	var wg sync.WaitGroup
	// go through list of jobs, assign them to next available worker
	for _, jobLength := range jobs {
		nextAvailableWorker := <-workerQueue
		wg.Add(1)
		go nextAvailableWorker.startWorkingOnJob(jobLength, workerQueue, &wg)
	}
	wg.Wait()
}
