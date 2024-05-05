import model
import repository
import datetime
import logger

def get_session_id():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Handler:
	def __init__(self, session_id, model, dataset, prompter, logger=logger.Logger(), repository=repository.Repository()) -> None:
		self.session_id = session_id
		self.model = model
		self.dataset = dataset
		self.prompter = prompter
		self.logger = logger
		self.repository = repository
	def run(self):
		self.logger.info('Starting handler')
		for sample in self.dataset:
			try:
				self.logger.info(f'Generating content for problem {sample.get_id()}')
				prompt = self.prompter.make(sample)
				content = model.generate_content(prompt)
				result = self.repository.insert(sample, content, self.session_id)
				logger.info(f'Generated content for problem {sample.get_id()}: {result}')
			except Exception as e:
				logger.error(f'Error generating content for problem {sample.get_id()}: {e}')

