
import overtime as ot

times = ['14:00','14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', '14:40', '14:45', '14:50', '14:55']
tfl_data = ot.TflInput(['victoria', 'central', 'bakerloo', 'piccadilly'], ['inbound', 'outbound'], times)
