from flask import Flask, render_template,abort
import numpy as np
import matplotlib.colors
import signal
import sys
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets, LogLevels
from brainflow.data_filter import DataFilter, WindowOperations, DetrendOperations

app = Flask(__name__)

# initialize Brainflow board
BoardShim.enable_dev_board_logger()
params = BrainFlowInputParams()
board_id = BoardIds.SYNTHETIC_BOARD.value # BoardIds.CYTON_BOARD.value
serial_port = '' # TODO
board_descr = BoardShim.get_board_descr(board_id)
sampling_rate = int(board_descr['sampling_rate'])
board = BoardShim(board_id, params)
board.prepare_session()
board.start_stream()

# Python Flask stuff
@app.route('/')
def index():
    """

    Renders the starter template where the color is white and there are no states associated
    with the 5 channels.
    """
    return render_template("dashboard.html", color="white", state="", n=5)

@app.route('/update')
def update():

    # get all data from buffer
    data = board.get_board_data()
    print(f'Got new data: {data.shape}')

    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    # nfft = DataFilter.get_nearest_power_of_two(sampling_rate // 2)
    # nfft = int(data.shape[1])

    # get band power values
    eeg_channels = board_descr['eeg_channels']
    # second eeg channel of synthetic board is a sine wave at 10Hz, should see huge alpha
    eeg_channel = eeg_channels[1]
    # optional detrend
    # DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
    psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                   WindowOperations.BLACKMAN_HARRIS.value)

    band_power_alpha = DataFilter.get_band_power(psd, 7.0, 13.0)
    band_power_beta = DataFilter.get_band_power(psd, 14.0, 30.0)
    band_power_gamma = DataFilter.get_band_power(psd, 30.0, 100.0)
    band_power_theta = DataFilter.get_band_power(psd, 4.0, 6.0)
    band_power_delta = DataFilter.get_band_power(psd, 0.5, 3.0)

    band_power_names = ["delta band power", "theta band power", "alpha band power", "beta band power", "gamma band power"]

    purples = matplotlib.colormaps['Purples'].resampled(100)
    blues = matplotlib.colormaps['Blues'].resampled(100)
    greens = matplotlib.colormaps['Greens'].resampled(100)
    oranges = matplotlib.colormaps['Oranges'].resampled(100)
    reds = matplotlib.colormaps['Reds'].resampled(100)

    max_delta = 40
    max_theta = 0.05
    max_alpha = 110
    max_beta = 0.1
    max_gamma = 1

    delta_colour = matplotlib.colors.to_hex(reds(min(band_power_delta/max_delta, 1)))
    theta_colur = matplotlib.colors.to_hex(oranges(min(band_power_theta/max_theta, 1)))
    alpha_colur = matplotlib.colors.to_hex(greens(min(band_power_alpha/max_alpha, 1)))
    beta_colour = matplotlib.colors.to_hex(blues(min(band_power_beta/max_beta, 1)))
    gamma_colour = matplotlib.colors.to_hex(purples(min(band_power_gamma/max_gamma, 1)))

    band_powers =[delta_colour, theta_colur, alpha_colur, beta_colour, gamma_colour]

    # # return band power values
    # colors = []
    # for _ in range(5):
    #     rgb = np.random.random(3)
    #     colors.append(matplotlib.colors.to_hex(rgb))

    return {'data': band_powers}

def handle_signal(signum, frame):
    print(f'\nQuitting (received signal {signum})')
    board.stop_stream()
    board.release_session()
    # do cleanup
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)
