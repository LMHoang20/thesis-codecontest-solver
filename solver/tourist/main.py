from entity.problem import Problem

TOTAL_LLM_CALLS_PER_PROBLEM = 100
TOTAL_LLM_CALLS_PER_ATTEMPT = 20

def multiple_attempts(attempts):
    def decorator(func):
        def wrapper(*args, **kwargs):
            exceptions = []
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    continue
        return wrapper
    return decorator

def brainstorm(editorialist, problem, num_of_editorials):
    return editorialist.inference(problem, num_of_editorials)

def extract_observations(extractor, problem, editorials):
    return extractor.inference(problem, editorials)

def verify_observations(verifier, problem, observations):
    return verifier.inference(problem, observations)

def implement(coder, problem, editorial):
    return coder.inference(problem, editorial)

def debug_public(judge, coder, problem, solution):
    tests = problem.get_tests(public=True, private=False, generated=False)
    result = verifier.judge(solution, tests)
    if result.good():
        return solution
    else:
        stdout = result.get_stdout()
        stderr = result.get_stderr()
        failed_test = result.get_failed_test()
        return coder.debug(solution, failed_test, stdout, stderr)
    return solution
            
def debug_private(verifier, coder, problem, solution, attempts):
    tests = problem.get_tests(public=False, private=True, generated=True)
    for _ in range(attempts):
        result = verifier.judge(solution, tests)
        if not result.good():
            solution = coder.kactl(solution)
        result = verifier.judge(solution, tests)
        if not result.good():
            continue
        break

def reflect(reflector, problem, solution, editorial, attempts):
    for _ in range(attempts):
        try:
            return reflector.inference(problem, solution, editorial)
        except Exception as e:
            continue



def solve(problem):
    # Step 1: Brainstorming
    obtained_insights = []
    for _ in range(SOLVE_ATTEMPTS):
        editorials = brainstorm(problem, insights, BRAINSTORM_ATTEMPTS)
        # Step 2: Filtering
        first_observations = extract_observations(problem, editorials, EXTRACT_ATTEMPTS)
        valid_observation_ids = verify_observations(problem, first_observations, VERIFY_ATTEMPTS)
        if len(valid_observation_ids) == 0:
            continue
        for id in valid_observation_ids:
            observation = first_observations[id]
            obtained_insights.append(observation)
        # Step 3: Coding
        public_tests = problem.get_tests(public=True, private=False, generated=False)
        all_tests = problem.get_tests(public=True, private=True, generated=True)
        for id in valid_observation_ids:
            editorial = editorials[id]
            solution = implement(problem, editorial)
            solution = debug_public(problem, editorial)
            solution = debug_private(problem, editorial)
            # Step 4: Reflecting
            insights = reflect(problem, solution, editorial)
            obtained_insights += insights

def main():
    pass

if __name__ == "__main__":
    main()