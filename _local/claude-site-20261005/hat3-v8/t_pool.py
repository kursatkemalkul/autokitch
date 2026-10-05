import multiprocessing as mp, os
def f(i):
    try:
        import cadquery
        return (i, "ok")
    except Exception as e:
        return (i, repr(e))
if __name__ == "__main__":
    with mp.get_context("spawn").Pool(int(os.environ.get("N","4"))) as p:
        print(p.map(f, range(int(os.environ.get("N","4")))))
