import os
import time
import numpy as np
import matplotlib.pyplot as plt

from imputegap.tools import utils
from imputegap.recovery.imputation import Imputation
from imputegap.recovery.manager import TimeSeries


class Benchmarking:
    """
    A class to evaluate the performance of imputation algorithms through benchmarking across datasets and scenarios.

    Methods
    -------
    _config_optimization():
        Configure and execute optimization for a selected imputation algorithm and contamination scenario.
    avg_results():
        Calculate average metrics (e.g., RMSE) across multiple datasets and algorithm runs.
    generate_matrix():
        Generate and save a heatmap visualization of RMSE scores for datasets and algorithms.
    generate_reports():
        Create detailed text-based reports summarizing metrics and timing results for all evaluations.
    generate_plots():
        Visualize metrics (e.g., RMSE, MAE) and timing (e.g., imputation, optimization) across scenarios and datasets.
    comprehensive_evaluation():
        Perform a complete benchmarking pipeline, including contamination, imputation, evaluation, and reporting.

    Example
    -------
    output : {'drift': {'mcar': {'mean': {'bayesian': {'0.05': {'scores': {'RMSE': 0.9234927128429051, 'MAE': 0.7219362152785619, 'MI': 0.0, 'CORRELATION': 0}, 'times': {'contamination': 0.0010309219360351562, 'optimization': 0, 'imputation': 0.0005755424499511719}}, '0.1': {'scores': {'RMSE': 0.9699990038879407, 'MAE': 0.7774057495176013, 'MI': 0.0, 'CORRELATION': 0}, 'times': {'contamination': 0.0020699501037597656, 'optimization': 0, 'imputation': 0.00048422813415527344}}, '0.2': {'scores': {'RMSE': 0.9914069853975623, 'MAE': 0.8134840739732964, 'MI': 0.0, 'CORRELATION': 0}, 'times': {'contamination': 0.007096290588378906, 'optimization': 0, 'imputation': 0.000461578369140625}}, '0.4': {'scores': {'RMSE': 1.0552448338389784, 'MAE': 0.7426695186604741, 'MI': 0.0, 'CORRELATION': 0}, 'times': {'contamination': 0.043192148208618164, 'optimization': 0, 'imputation': 0.0005095005035400391}}, '0.6': {'scores': {'RMSE': 1.0143105930114702, 'MAE': 0.7610548321723654, 'MI': 0.0, 'CORRELATION': 0}, 'times': {'contamination': 0.17184901237487793, 'optimization': 0, 'imputation': 0.0005536079406738281}}, '0.8': {'scores': {'RMSE': 1.010712060535523, 'MAE': 0.7641520748788702, 'MI': 0.0, 'CORRELATION': 0}, 'times': {'contamination': 0.6064670085906982, 'optimization': 0, 'imputation': 0.0005743503570556641}}}}, 'cdrec': {'bayesian': {'0.05': {'scores': {'RMSE': 0.23303624184873978, 'MAE': 0.13619797235197734, 'MI': 1.2739817718416822, 'CORRELATION': 0.968435455112644}, 'times': {'contamination': 0.0009615421295166016, 'optimization': 0, 'imputation': 0.09218788146972656}}, '0.1': {'scores': {'RMSE': 0.18152059329152104, 'MAE': 0.09925566629402761, 'MI': 1.1516089897042538, 'CORRELATION': 0.9829398352220718}, 'times': {'contamination': 0.00482487678527832, 'optimization': 0, 'imputation': 0.09549617767333984}}, '0.2': {'scores': {'RMSE': 0.13894771223733138, 'MAE': 0.08459032692102293, 'MI': 1.186191167936035, 'CORRELATION': 0.9901338133811375}, 'times': {'contamination': 0.01713728904724121, 'optimization': 0, 'imputation': 0.1129295825958252}}, '0.4': {'scores': {'RMSE': 0.7544523683503829, 'MAE': 0.11218049973594252, 'MI': 0.021165172206064526, 'CORRELATION': 0.814120507570725}, 'times': {'contamination': 0.10881781578063965, 'optimization': 0, 'imputation': 1.9378046989440918}}, '0.6': {'scores': {'RMSE': 0.4355197572001326, 'MAE': 0.1380846624733049, 'MI': 0.10781252370591506, 'CORRELATION': 0.9166777087122915}, 'times': {'contamination': 0.2380077838897705, 'optimization': 0, 'imputation': 1.8785057067871094}}, '0.8': {'scores': {'RMSE': 0.7672558930795506, 'MAE': 0.32988968428439397, 'MI': 0.013509125598802707, 'CORRELATION': 0.7312998041323675}, 'times': {'contamination': 0.6805167198181152, 'optimization': 0, 'imputation': 1.9562773704528809}}}}, 'stmvl': {'bayesian': {'0.05': {'scores': {'RMSE': 0.5434405584289141, 'MAE': 0.346560495723809, 'MI': 0.7328867182584357, 'CORRELATION': 0.8519431955571422}, 'times': {'contamination': 0.0022056102752685547, 'optimization': 0, 'imputation': 52.07010293006897}}, '0.1': {'scores': {'RMSE': 0.39007056542870916, 'MAE': 0.2753022759369617, 'MI': 0.8280959876205578, 'CORRELATION': 0.9180937736429735}, 'times': {'contamination': 0.002231597900390625, 'optimization': 0, 'imputation': 52.543020248413086}}, '0.2': {'scores': {'RMSE': 0.37254427425455994, 'MAE': 0.2730547993858495, 'MI': 0.7425412593844177, 'CORRELATION': 0.9293322959355041}, 'times': {'contamination': 0.0072672367095947266, 'optimization': 0, 'imputation': 52.88247036933899}}, '0.4': {'scores': {'RMSE': 0.6027573766269363, 'MAE': 0.34494332493982044, 'MI': 0.11876685901414151, 'CORRELATION': 0.8390532279447225}, 'times': {'contamination': 0.04321551322937012, 'optimization': 0, 'imputation': 54.10793352127075}}, '0.6': {'scores': {'RMSE': 0.9004526656857551, 'MAE': 0.4924048353228427, 'MI': 0.011590260996247858, 'CORRELATION': 0.5650541301828254}, 'times': {'contamination': 0.1728806495666504, 'optimization': 0, 'imputation': 40.53373336791992}}, '0.8': {'scores': {'RMSE': 1.0112488396023014, 'MAE': 0.7646823531588104, 'MI': 0.00040669209664367576, 'CORRELATION': 0.0183962968474991}, 'times': {'contamination': 0.6077785491943359, 'optimization': 0, 'imputation': 35.151907444000244}}}}, 'iim': {'bayesian': {'0.05': {'scores': {'RMSE': 0.4445625930776235, 'MAE': 0.2696133927362288, 'MI': 1.1167751522591498, 'CORRELATION': 0.8944975075266335}, 'times': {'contamination': 0.0010058879852294922, 'optimization': 0, 'imputation': 0.7380530834197998}}, '0.1': {'scores': {'RMSE': 0.2939506418814281, 'MAE': 0.16953644212278182, 'MI': 1.0160968166750064, 'CORRELATION': 0.9531900627237018}, 'times': {'contamination': 0.0019745826721191406, 'optimization': 0, 'imputation': 4.7826457023620605}}, '0.2': {'scores': {'RMSE': 0.2366529609250008, 'MAE': 0.14709529129218185, 'MI': 1.064299483512458, 'CORRELATION': 0.9711348247027318}, 'times': {'contamination': 0.00801849365234375, 'optimization': 0, 'imputation': 33.94813060760498}}, '0.4': {'scores': {'RMSE': 0.4155649406397416, 'MAE': 0.22056702659999994, 'MI': 0.06616526470761779, 'CORRELATION': 0.919934494058292}, 'times': {'contamination': 0.04391813278198242, 'optimization': 0, 'imputation': 255.31524085998535}}, '0.6': {'scores': {'RMSE': 0.38695094864012947, 'MAE': 0.24340565131372927, 'MI': 0.06361822797740405, 'CORRELATION': 0.9249744935121553}, 'times': {'contamination': 0.17044353485107422, 'optimization': 0, 'imputation': 840.7470128536224}}, '0.8': {'scores': {'RMSE': 0.5862696375344495, 'MAE': 0.3968159514130716, 'MI': 0.13422239939628303, 'CORRELATION': 0.8178796825899766}, 'times': {'contamination': 0.5999574661254883, 'optimization': 0, 'imputation': 1974.6101157665253}}}}, 'mrnn': {'bayesian': {'0.05': {'scores': {'RMSE': 0.9458508648057621, 'MAE': 0.7019459696903068, 'MI': 0.11924522547609226, 'CORRELATION': 0.02915935932568557}, 'times': {'contamination': 0.001056671142578125, 'optimization': 0, 'imputation': 49.42237901687622}}, '0.1': {'scores': {'RMSE': 1.0125309431502871, 'MAE': 0.761136543268339, 'MI': 0.12567590499764303, 'CORRELATION': -0.037161060882302754}, 'times': {'contamination': 0.003415822982788086, 'optimization': 0, 'imputation': 49.04829454421997}}, '0.2': {'scores': {'RMSE': 1.0317754516097355, 'MAE': 0.7952869439926, 'MI': 0.10908095436833125, 'CORRELATION': -0.04155403791391449}, 'times': {'contamination': 0.007429599761962891, 'optimization': 0, 'imputation': 49.42568325996399}}, '0.4': {'scores': {'RMSE': 1.0807965786089415, 'MAE': 0.7326965517264863, 'MI': 0.006171770470542263, 'CORRELATION': -0.020630168509677818}, 'times': {'contamination': 0.042899370193481445, 'optimization': 0, 'imputation': 49.479795694351196}}, '0.6': {'scores': {'RMSE': 1.0441472017887297, 'MAE': 0.7599852461729673, 'MI': 0.01121013333181846, 'CORRELATION': -0.007513931343350665}, 'times': {'contamination': 0.17329692840576172, 'optimization': 0, 'imputation': 50.439927101135254}}, '0.8': {'scores': {'RMSE': 1.0379347892718205, 'MAE': 0.757440007226372, 'MI': 0.0035880775657246428, 'CORRELATION': -0.0014975078469404196}, 'times': {'contamination': 0.6166613101959229, 'optimization': 0, 'imputation': 50.66455388069153}}}}}}}
    """

    def _config_optimization(self, opti_mean, ts_test, scenario, algorithm, block_size_mcar):
        """
        Configure and execute optimization for selected imputation algorithm and scenario.

        Parameters
        ----------
        opti_mean : float
            Mean parameter for contamination.
        ts_test : TimeSeries
            TimeSeries object containing dataset.
        scenario : str
            Type of contamination scenario (e.g., "mcar", "mp", "blackout").
        algorithm : str
            Imputation algorithm to use.
        block_size_mcar : int
            Size of blocks removed in MCAR

        Returns
        -------
        BaseImputer
            Configured imputer instance with optimal parameters.
        """

        if scenario == "mcar":
            infected_matrix_opti = ts_test.Contamination.mcar(input_data=ts_test.data, series_rate=opti_mean,
                                                              missing_rate=opti_mean, block_size=block_size_mcar,
                                                              use_seed=True, seed=42)
        elif scenario == "mp":
            infected_matrix_opti = ts_test.Contamination.missing_percentage(input_data=ts_test.data, series_rate=opti_mean,
                                                                            missing_rate=opti_mean)
        else:
            infected_matrix_opti = ts_test.Contamination.blackout(input_data=ts_test.data, missing_rate=opti_mean)

        i_opti = None
        if algorithm == "cdrec":
            i_opti = Imputation.MatrixCompletion.CDRec(infected_matrix_opti)
        elif algorithm == "stmvl":
            i_opti = Imputation.PatternSearch.STMVL(infected_matrix_opti)
        elif algorithm == "iim":
            i_opti = Imputation.Statistics.IIM(infected_matrix_opti)
        elif algorithm == "mrnn":
            i_opti = Imputation.DeepLearning.MRNN(infected_matrix_opti)
        elif algorithm == "mean":
            i_opti = Imputation.Statistics.MeanImpute(infected_matrix_opti)

        return i_opti

    def avg_results(self, *datasets):
        """
        Calculate the average of all metrics and times across multiple datasets.

        Parameters
        ----------
        datasets : dict
            Multiple dataset dictionaries to be averaged.

        Returns
        -------
        dict
            Dictionary with averaged scores and times for all levels.
        """

        # Step 1: Compute average RMSE across runs for each dataset and algorithm
        aggregated_data = {}

        for runs in datasets:
            for dataset, dataset_items in runs.items():
                if dataset not in aggregated_data:
                    aggregated_data[dataset] = {}

                for scenario, scenario_items in dataset_items.items():
                    for algo, algo_data in scenario_items.items():
                        if algo not in aggregated_data[dataset]:
                            aggregated_data[dataset][algo] = []

                        for missing_values, missing_values_item in algo_data.items():
                            for param, param_data in missing_values_item.items():
                                rmse = param_data["scores"]["RMSE"]
                                aggregated_data[dataset][algo].append(rmse)

        # Step 2: Compute averages using NumPy
        average_rmse_matrix = {}
        for dataset, algos in aggregated_data.items():
            average_rmse_matrix[dataset] = {}
            for algo, rmse_values in algos.items():
                rmse_array = np.array(rmse_values)
                avg_rmse = np.mean(rmse_array)
                average_rmse_matrix[dataset][algo] = avg_rmse

        # Step 3: Create a matrix representation of datasets and algorithms
        datasets_list = list(average_rmse_matrix.keys())
        algorithms = {algo for algos in average_rmse_matrix.values() for algo in algos}
        algorithms_list = sorted(algorithms)

        # Prepare a NumPy matrix
        comprehensive_matrix = np.zeros((len(datasets_list), len(algorithms_list)))

        for i, dataset in enumerate(datasets_list):
            for j, algo in enumerate(algorithms_list):
                comprehensive_matrix[i, j] = average_rmse_matrix[dataset].get(algo, np.nan)

        print("Visualization of datasets:", datasets_list)
        print("Visualization of algorithms:", algorithms_list)
        print("Visualization of matrix:\n", comprehensive_matrix)

        return comprehensive_matrix, algorithms_list, datasets_list

    def generate_matrix(self, scores_list, algos, sets, save_dir="./reports", display=True):
        """
        Generate and save RMSE matrix in HD quality.

        Parameters
        ----------
        scores_list : np.ndarray
            2D numpy array containing RMSE values.
        algos : list of str
            List of algorithm names (columns of the heatmap).
        sets : list of str
            List of dataset names (rows of the heatmap).
        save_dir : str, optional
            Directory to save the generated plot (default is "./reports").
        display : bool, optional
            Display or not the plot

        Returns
        -------
        Bool
            True if the matrix has been generated
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        fig, ax = plt.subplots(figsize=(10, 6))
        cmap = plt.cm.Greys
        norm = plt.Normalize(vmin=0, vmax=2)  # Normalizing values between 0 and 2 (RMSE)

        # Create the heatmap
        heatmap = ax.imshow(scores_list, cmap=cmap, norm=norm, aspect='auto')

        # Add color bar for reference
        cbar = plt.colorbar(heatmap, ax=ax, orientation='vertical')
        cbar.set_label('RMSE', rotation=270, labelpad=15)

        # Set the tick labels
        ax.set_xticks(np.arange(len(algos)))
        ax.set_xticklabels(algos)
        ax.set_yticks(np.arange(len(sets)))
        ax.set_yticklabels(sets)

        # Add titles and labels
        ax.set_title('ImputeGAP Algorithms Comparison')
        ax.set_xlabel('Algorithms')
        ax.set_ylabel('Datasets')

        # Show values on the heatmap
        for i in range(len(sets)):
            for j in range(len(algos)):
                ax.text(j, i, f"{scores_list[i, j]:.2f}",
                        ha='center', va='center',
                        color="black" if scores_list[i, j] < 1 else "white")  # for visibility

        filename = f"benchmarking_rmse.jpg"
        filepath = os.path.join(save_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')  # Save in HD with tight layout

        # Show the plot
        if display :
            plt.tight_layout()
            plt.show()
            plt.close()

        return True

    def generate_reports(self, runs_plots_scores, save_dir="./reports", dataset=""):
        """
        Generate and save a text reports of metrics and timing for each dataset, algorithm, and scenario.

        Parameters
        ----------
        runs_plots_scores : dict
            Dictionary containing scores and timing information for each dataset, scenario, and algorithm.
        save_dir : str, optional
            Directory to save the reports file (default is "./reports").
        dataset : str, optional
            Name of the data for the reports name.

        Returns
        -------
        None

        Notes
        -----
        The reports is saved in a "reports.txt" file in `save_dir`, organized in tabular format.
        """

        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, "report_" + str(dataset) + ".txt")
        with open(save_path, "w") as file:
            file.write("dictionary of results : " + str(runs_plots_scores) + "\n\n")

            # Define header with time columns included
            header = "| dataset_value | algorithm_value | optimizer_value | scenario_value | x_value | RMSE | MAE | MI | CORRELATION | time_contamination | time_optimization | time_imputation |\n"
            file.write(header)

            for dataset, algo_items in runs_plots_scores.items():
                for algorithm, optimizer_items in algo_items.items():
                    for optimizer, scenario_data in optimizer_items.items():
                        for scenario, x_data_items in scenario_data.items():
                            for x, values in x_data_items.items():
                                metrics = values["scores"]
                                times = values["times"]

                                # Retrieve each timing value, defaulting to None if absent
                                contamination_time = times.get("contamination", None)
                                optimization_time = times.get("optimization", None)
                                imputation_time = times.get("imputation", None)

                                # Create a reports line with timing details
                                line = (
                                    f"| {dataset} | {algorithm} | {optimizer} | {scenario} | {x} "
                                    f"| {metrics.get('RMSE')} | {metrics.get('MAE')} | {metrics.get('MI')} "
                                    f"| {metrics.get('CORRELATION')} | {contamination_time} sec | {optimization_time} sec"
                                    f"| {imputation_time} sec |\n"
                                )
                                file.write(line)

        print("\nReport recorded in", save_path)

    def generate_plots(self, runs_plots_scores, s="M", v="N", save_dir="./reports"):
        """
        Generate and save plots for each metric and scenario based on provided scores.

        Parameters
        ----------
        runs_plots_scores : dict
            Dictionary containing scores and timing information for each dataset, scenario, and algorithm.
        s : str
            display the number of series in graphs
        v : sts
            display the number of values in graphs
        save_dir : str, optional
            Directory to save generated plots (default is "./reports").

        Returns
        -------
        None

        Notes
        -----
        Saves generated plots in `save_dir`, categorized by dataset, scenario, and metric.
        """
        os.makedirs(save_dir, exist_ok=True)

        for dataset, scenario_items in runs_plots_scores.items():
            for scenario, algo_items in scenario_items.items():
                # Iterate over each metric, generating separate plots, including new timing metrics
                for metric in ["RMSE", "MAE", "MI", "CORRELATION", "imputation_time", "optimization_time",
                               "contamination_time"]:
                    plt.figure(figsize=(10, 4))  # Fixed height set by second parameter
                    has_data = False  # Flag to check if any data is added to the plot

                    # Iterate over each algorithm and plot them in the same figure
                    for algorithm, optimizer_items in algo_items.items():
                        x_vals = []
                        y_vals = []
                        for optimizer, x_data in optimizer_items.items():
                            for x, values in x_data.items():
                                # Differentiate between score metrics and timing metrics
                                if metric == "imputation_time" and "imputation" in values["times"]:
                                    x_vals.append(float(x))
                                    y_vals.append(values["times"]["imputation"])
                                elif metric == "optimization_time" and "optimization" in values["times"]:
                                    x_vals.append(float(x))
                                    y_vals.append(values["times"]["optimization"])
                                elif metric == "contamination_time" and "contamination" in values["times"]:
                                    x_vals.append(float(x))
                                    y_vals.append(values["times"]["contamination"])
                                elif metric in values["scores"]:
                                    x_vals.append(float(x))
                                    y_vals.append(values["scores"][metric])

                        # Only plot if there are values to plot
                        if x_vals and y_vals:
                            # Sort x and y values by x for correct spacing
                            sorted_pairs = sorted(zip(x_vals, y_vals))
                            x_vals, y_vals = zip(*sorted_pairs)

                            # Plot each algorithm as a line with scattered points
                            plt.plot(x_vals, y_vals, label=f"{algorithm}")
                            plt.scatter(x_vals, y_vals)
                            has_data = True

                    # Save plot only if there is data to display
                    if has_data:
                        # Set plot titles and labels based on metric
                        title_metric = {
                            "imputation_time": "Imputation Time",
                            "optimization_time": "Optimization Time",
                            "contamination_time": "Contamination Time"
                        }.get(metric, metric)
                        ylabel_metric = {
                            "imputation_time": "Imputation Time (seconds)",
                            "optimization_time": "Optimization Time (seconds)",
                            "contamination_time": "Contamination Time (seconds)"
                        }.get(metric, metric)

                        plt.title(f"{dataset} | {scenario} | {title_metric} | ({s}x{v})")
                        plt.xlabel(f"{scenario} rate of missing values and missing series")
                        plt.ylabel(ylabel_metric)
                        plt.xlim(0.0, 0.85)

                        # Set y-axis limits with padding below 0 for visibility
                        if metric == "imputation_time":
                            plt.ylim(-10, 90)
                        elif metric == "contamination_time":
                            plt.ylim(-0.01, 0.59)
                        elif metric == "MAE":
                            plt.ylim(-0.1, 2.4)
                        elif metric == "MI":
                            plt.ylim(-0.1, 1.85)
                        elif metric == "RMSE":
                            plt.ylim(-0.1, 2.6)
                        elif metric == "CORRELATION":
                            plt.ylim(-0.75, 1.1)

                        # Customize x-axis ticks
                        x_points = [0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8]
                        plt.xticks(x_points, [f"{int(tick * 100)}%" for tick in x_points])
                        plt.grid(True, zorder=0)
                        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

                        # Define a unique filename
                        filename = f"{dataset}_{scenario}_{metric}.jpg"
                        filepath = os.path.join(save_dir, filename)

                        # Save the figure
                        plt.savefig(filepath)
                    plt.close()  # Close to avoid memory issues

        print("\nAll plots recorded in", save_dir)

    def comprehensive_evaluation(self, datasets=[], optimizers=[], algorithms=[], scenarios=[],
                                 x_axis=[0.05, 0.1, 0.2, 0.4, 0.6, 0.8], save_dir="./reports", already_optimized=False,
                                 reports=1):
        """
        Execute a comprehensive evaluation of imputation algorithms over multiple datasets and scenarios.

        Parameters
        ----------
        datasets : list of str
            List of dataset names to evaluate.
        optimizers : list of dict
            List of optimizers with their configurations.
        algorithms : list of str
            List of imputation algorithms to test.
        scenarios : list of str
            List of contamination scenarios to apply.
        x_axis : list of float
            List of missing rates for contamination.
        save_dir : str, optional
            Directory to save reports and plots (default is "./reports").
        already_optimized : bool, optional
            If True, skip parameter optimization (default is False).
        reports : int, optional
            Number of executions with a view to averaging them

        Returns
        -------
        None

        Notes
        -----
        Runs contamination, imputation, and evaluation, then generates plots and a summary reports.
        """

        print("initialization of the comprehensive evaluation. It can take time...\n")

        for runs in range(0, abs(reports)):
            for dataset in datasets:
                runs_plots_scores = {}
                limitation_series, limitation_values = 100, 1000
                block_size_mcar = 10

                print("1. evaluation launch for", dataset,
                      "========================================================\n\n\n")
                ts_test = TimeSeries()

                header = False
                if dataset == "eeg-reading":
                    header = True
                elif dataset == "drift":
                    limitation_series = 50
                elif dataset == "fmri-objectviewing":
                    limitation_series = 360
                elif dataset == "fmri-stoptask":
                    limitation_series = 360

                if reports == -1:
                    limitation_series = 10
                    limitation_values = 110
                    print("TEST LOADED...")

                ts_test.load_timeseries(data=utils.search_path(dataset), max_series=limitation_series,
                                        max_values=limitation_values, header=header)

                start_time_opti, end_time_opti = 0, 0
                M, N = ts_test.data.shape

                if N < 250:
                    block_size_mcar = 2

                print("1. normalization of ", dataset, "\n")
                ts_test.normalize()

                for scenario in scenarios:
                    print("\t2. contamination of", dataset, "with scenario", scenario, "\n")

                    for algorithm in algorithms:
                        has_been_optimized = False
                        print("\t3. algorithm selected", algorithm, "\n")

                        for x in x_axis:
                            print("\t\t4. missing values (series&values) set to", x, "for x_axis\n")

                            start_time_contamination = time.time()  # Record start time
                            if scenario == "mcar":
                                infected_matrix = ts_test.Contamination.mcar(input_data=ts_test.data, series_rate=x,
                                                                             missing_rate=x, block_size=block_size_mcar,
                                                                             use_seed=True, seed=42)
                            elif scenario == "mp":
                                infected_matrix = ts_test.Contamination.missing_percentage(input_data=ts_test.data,
                                                                                           series_rate=x,
                                                                                           missing_rate=x)
                            else:
                                infected_matrix = ts_test.Contamination.blackout(input_data=ts_test.data, missing_rate=x)
                            end_time_contamination = time.time()

                            for optimizer in optimizers:
                                algo = None
                                optimizer_gt = {"ground_truth": ts_test.data, **optimizer}
                                if algorithm == "cdrec":
                                    algo = Imputation.MatrixCompletion.CDRec(infected_matrix)
                                elif algorithm == "stmvl":
                                    algo = Imputation.PatternSearch.STMVL(infected_matrix)
                                elif algorithm == "iim":
                                    algo = Imputation.Statistics.IIM(infected_matrix)
                                elif algorithm == "mrnn":
                                    algo = Imputation.DeepLearning.MRNN(infected_matrix)
                                elif algorithm == "mean":
                                    algo = Imputation.Statistics.MeanImpute(infected_matrix)

                                if not has_been_optimized and not already_optimized and algorithm != "mean":
                                    print("\t\t5. AutoML to set the parameters", optimizer, "\n")
                                    start_time_opti = time.time()  # Record start time
                                    i_opti = self._config_optimization(0.25, ts_test, scenario, algorithm,
                                                                       block_size_mcar)
                                    i_opti.impute(user_def=False, params=optimizer_gt)
                                    utils.save_optimization(optimal_params=i_opti.parameters, algorithm=algorithm,
                                                            dataset=dataset, optimizer="e")
                                    has_been_optimized = True
                                    end_time_opti = time.time()

                                if algorithm != "mean":
                                    opti_params = utils.load_parameters(query="optimal", algorithm=algorithm,
                                                                        dataset=dataset, optimizer="e")
                                    print("\t\t6. imputation", algorithm, "with optimal parameters", *opti_params)

                                else:
                                    opti_params = None

                                start_time_imputation = time.time()
                                algo.impute(params=opti_params)
                                end_time_imputation = time.time()

                                algo.score(input_data=ts_test.data, recov_data=algo.imputed_matrix)

                                time_contamination = end_time_contamination - start_time_contamination
                                time_opti = end_time_opti - start_time_opti
                                time_imputation = end_time_imputation - start_time_imputation

                                dic_timing = {"contamination": time_contamination, "optimization": time_opti,
                                              "imputation": time_imputation}

                                dataset_s = dataset
                                if "-" in dataset:
                                    dataset_s = dataset.replace("-", "")

                                optimizer_value = optimizer.get('optimizer')  # or optimizer['optimizer']

                                runs_plots_scores.setdefault(str(dataset_s), {}).setdefault(str(scenario),
                                                                                            {}).setdefault(
                                    str(algorithm), {}).setdefault(str(optimizer_value), {})[str(x)] = {
                                    "scores": algo.metrics,
                                    "times": dic_timing
                                }

                                print("\t\truns_plots_scores", runs_plots_scores)

                print("\truns_plots_scores : ", runs_plots_scores)
                save_dir_runs = save_dir + "/report_" + str(runs)
                print("\truns saved in : ", save_dir_runs)
                self.generate_plots(runs_plots_scores=runs_plots_scores, s=str(M), v=str(N), save_dir=save_dir_runs)
                self.generate_reports(runs_plots_scores, save_dir_runs, dataset)

                print(
                    "======================================================================================\n\n\n\n\n\n")

        return runs_plots_scores
