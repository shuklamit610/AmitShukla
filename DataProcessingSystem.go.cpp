package main

import (
    "fmt"
    "sync"
    "time"
)

type Task struct {
    id int
}

func processTask(task Task) (int, error) {
    time.Sleep(500 * time.Millisecond) // simulate work
    return task.id * 2, nil
}

func worker(id int, tasks <-chan Task, results chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()

    for task := range tasks {
        fmt.Printf("Worker %d processing task %d\n", id, task.id)

        result, err := processTask(task)
        if err != nil {
            fmt.Println("Error:", err)
            continue
        }

        results <- result
    }
}

func main() {
    tasks := make(chan Task, 10)
    results := make(chan int, 10)

    var wg sync.WaitGroup

    // Start workers
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go worker(i, tasks, results, &wg)
    }

    // Add tasks
    for i := 1; i <= 10; i++ {
        tasks <- Task{id: i}
    }
    close(tasks)

    wg.Wait()
    close(results)

    for result := range results {
        fmt.Println("Result:", result)
    }
}