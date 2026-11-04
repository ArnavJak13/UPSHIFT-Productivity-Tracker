from tests.test_database import run_database_tests
from tests.test_analytics import run_analytics_tests


print("Running UPSHIFT tests...")
run_database_tests()
run_analytics_tests()
print("All tests passed")
