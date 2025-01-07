PROGRAM test_f_barrier
  use mpi
  use iso_fortran_env
  use omp_lib
  use oomph_mod

  implicit none  

  integer :: mpi_err
  integer :: mpi_threading, mpi_size, mpi_rank
  integer :: nthreads = 1

  !$omp parallel shared(nthreads)
  nthreads = omp_get_num_threads()
  !$omp end parallel

  if (nthreads==1) then
    call mpi_init_thread (MPI_THREAD_SINGLE, mpi_threading, mpi_err)
  else
    call mpi_init_thread (MPI_THREAD_MULTIPLE, mpi_threading, mpi_err)
    if (MPI_THREAD_MULTIPLE /= mpi_threading) then
      stop "MPI does not support multithreading"
    end if
  end if
  call mpi_comm_size (mpi_comm_world, mpi_size, mpi_err)
  call mpi_comm_rank (mpi_comm_world, mpi_rank, mpi_err)

  if (mpi_rank==0) then
    print *, mpi_size, "ranks and", nthreads, "threads per rank"
  end if
  
  ! init oomph
  call oomph_init(nthreads, mpi_comm_world);

  !$omp parallel

  ! call MT barrier
  call oomph_barrier(OomphBarrierGlobal)

  ! rank barrier
  call oomph_barrier(OomphBarrierRank)

  ! thread barrier
  call oomph_barrier(OomphBarrierThread)

  !$omp end parallel

  if (mpi_rank==0) then
    print *, "result: OK"
  end if

  call oomph_finalize()  
  call mpi_finalize(mpi_err)

END PROGRAM test_f_barrier
