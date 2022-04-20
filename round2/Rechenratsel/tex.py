examples = {}

with open("examples.txt", "r", encoding="utf-8") as f:
    examples_ = f.read().split("\n")
    for example in examples_:
        if example == "":
            continue

        raw_n, raw_therm = example.split(": ")
        raw_therm, raw_time = raw_therm.split("; ")
        exercise, solution = raw_therm.split(" | ")

        n, time = int(raw_n), float(raw_time)

        if n not in examples:
            examples[n] = []

        examples[n].append((exercise, solution, time))

for i in range(16):
    if i not in examples:
        continue

    print("\\paragraph{$n="+str(i)+"$} \\hrulefill\n\\\\")
    for exercise, solution, time in examples[i][:3]:
        print("\\\\")
        print(exercise + "\\\\")
        print(solution + "\\\\")
        print(f"{time:.2f} Sekunden\\\\")

