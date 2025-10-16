**Step-by-Step Guide: MPI \& OpenMP Programs**

**1. Update your system**

sudo apt update

sudo apt upgrade -y





**2. Install necessary compilers**



a) GCC for C and OpenMP\*



sudo apt install build-essential -y



This installs gcc, g++, make, etc.



b) MPI (MPICH)



sudo apt install mpich -y





This installs:



\* mpicc → C MPI compiler

\* mpic++ → C++ MPI compiler

\* mpirun → to run MPI programs



**3. Create the OpenMP program**



File: openmp\_max.c



c

\#include <stdio.h>

\#include <omp.h>

int main(void){

    int arr\[10] = {2, 77, 45, 18, 7, 264, 183, 23, 55, 90};

    int n = 10;

    int max = arr\[0];

    #pragma omp parallel for reduction(max:max)

    for(int i = 1; i < n; i++){

        if(arr\[i] > max){

            max = arr\[i];

        }

    }

    printf("Largest Number is %d\\n", max);

    return 0;

}



Compile and Run OpenMP



gcc -fopenmp openmp\_max.c -o openmp\_max   # Compile



./openmp\_max                             # Run



Expected Output:

Largest Number is 264



**4. Create the MPI program**



File: mpi\_max.cpp



cpp

\#include <stdio.h>

\#include <mpi.h>

int main(int argc, char\* argv\[]){

    int n = 10;

    int rank, size;

    int arr\[10] = {2, 77, 45, 18, 7, 264, 183, 23, 55, 90};

    MPI\_Init(\&argc, \&argv);

    MPI\_Comm\_rank(MPI\_COMM\_WORLD, \&rank);

    MPI\_Comm\_size(MPI\_COMM\_WORLD, \&size);

    int chunks = n / size;

    int start = chunks \* rank;

    int end = (rank == size - 1) ? n : start + chunks;

    int local\_max = arr\[start];

    for(int i = start; i < end; i++){

        if(local\_max < arr\[i]){

            local\_max = arr\[i];

        }

    }

    int global\_max;

    MPI\_Reduce(\&local\_max, \&global\_max, 1, MPI\_INT, MPI\_MAX, 0, MPI\_COMM\_WORLD);

    if(rank == 0){

        printf("Largest Number is %d\\n", global\_max);

    }

    MPI\_Finalize();

    return 0;

}



Compile and Run MPI



mpic++ mpi\_max.cpp -o mpi\_max       # Compile with MPI C++

mpirun -np 4 ./mpi\_max             # Run with 4 processes





Expected Output:



Largest Number is 264



**5. Optional: Clean invisible characters**



If you copied code from the web, sometimes return 0; may have invisible characters. Remove them with:



tr -d '\\r\\u00a0' < mpi\_max.cpp > clean.cpp \&\& mv clean.cpp mpi\_max.cpp





**6. Notes**



OpenMP uses threads; MPI uses processes.

You can combine both for \*hybrid parallelism\* (MPI + OpenMP).

For larger arrays, both programs will scale better with more threads or processes.

