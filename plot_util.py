import os, re
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from playground.Non_DAG.utils.common_tokens import *
from scipy.stats import pearsonr, spearmanr, kendalltau

total_iters = 180


def load_df(csv_path=None, ignore_idx=False):
    if csv_path and os.path.exists(csv_path):
        if ignore_idx:
            df = pd.read_csv(csv_path, index_col=[0])
        else:
            df = pd.read_csv(csv_path)
        return df


def rename_df_col(df, prefix="", save_to=""):
    if not df is None:
        cols = df.columns.values.tolist()
        df_renamed = pd.DataFrame()
        for col in cols:
            if col and col != "Unnamed: 0":
                new_name = f"{prefix}{col}"
                df_renamed[new_name] = df[col]
            else:
                df_renamed[col] = df[col]
        if save_to:
            df_renamed.to_csv(save_to, index=False)


def get_corr_pvalue(x, y, corr_type="pearsonr", col_value=""):
    if x and y:
        try:
            if corr_type == "pearsonr":
                return pearsonr(x, y)
            elif corr_type == "spearmanr":
                return spearmanr(x, y)
            elif corr_type == "kendalltau":
                return kendalltau(x, y)
        except Exception as e:
            print(e)
            print("colvalue cause the error:", col_value)
            print(f"corr type: {corr_type}")
            print(f'x type: {type(x)} ; y type: {type(y)}')
            print(x)
            print(y)


def rename_add_reward_type():
    """
    rename column name for plotting later
    only need to do it once
    :return:
    """
    is_original = True
    hist_completions = get_exp_file_path(file_type=avg_completions, is_original=is_original)
    hist_makespans = get_exp_file_path(file_type=avg_makespans, is_original=is_original)
    hist_slowdowns = get_exp_file_path(file_type=avg_slowdowns, is_original=is_original)
    df_completions = load_df(hist_completions)
    df_makespans = load_df(hist_makespans)
    df_slowdowns = load_df(hist_slowdowns)
    # rename_df_col(df_completions, prefix=reward_avg_completions + "_",
    #               save_to=get_exp_file_path(file_type=avg_completions, is_original=False))
    # rename_df_col(df_makespans, prefix=reward_avg_makespans + "_",
    #               save_to=get_exp_file_path(file_type=avg_makespans, is_original=False))
    rename_df_col(df_slowdowns, prefix=reward_avg_slowdowns + "_",
                  save_to=get_exp_file_path(file_type=avg_slowdowns, is_original=False))
    print(f"renamed columns.")


def plot_lines_from_df(df, cols=None, title=None, y_label=None):
    # if not cols is None:
    #     cols = df.columns.values.tolist()
    fig = plt.figure()
    num_sub_plots = 1
    gs = fig.add_gridspec(num_sub_plots, hspace=0)
    # axs = gs.subplots(sharex=True, sharey=True)
    axs = gs.subplots()
    # fig.suptitle("this is the super title")

    figsize = (8, 8)
    if num_sub_plots == 1:
        # df.plot(marker='.', figsize=figsize, ax=axs, color=get_column_color(df1))
        df.plot(marker='.', figsize=figsize, ax=axs)
    if title:
        axs.set_title(title)
    if y_label:
        axs.set_ylabel(y_label)
    # for ax in axs:
    #     ax.label_outer()
    # plt.savefig(save_to)
    plt.show()


def plot_all_job_stats_from_df(df, cols=None, show_y_lable=True, save_to=None):
    if cols is None:
        return
    fig = plt.figure()
    num_sub_plots = len(cols)
    gs = fig.add_gridspec(1, num_sub_plots, hspace=0)
    # axs = gs.subplots(sharex=True, sharey=True)
    axs = gs.subplots(sharex=True, sharey=False)
    # fig.suptitle("this is the super title")

    figsize = (24, 8)
    if num_sub_plots == 1:
        # df.plot(marker='.', figsize=figsize, ax=axs, color=get_column_color(df1))
        df.plot(figsize=figsize, ax=axs)
    else:
        for idx, col in enumerate(cols):
            df[col].plot(figsize=figsize, ax=axs[idx])
            if show_y_lable:
                lable = col.capitalize() if col != "instances_num" else "Number of Instances"
                axs[idx].set_ylabel(lable)
    # for ax in axs:
    #     ax.label_outer()
    if save_to:
        fpath = os.path.join(save_to, "job_stats_all.png")
        plt.savefig(fpath)
    else:
        plt.show()


def plot_individual_job_stats_from_df(df, cols=None, show_y_lable=True, save_to=None):
    if cols is None:
        return
    fig = plt.figure()
    num_sub_plots = 1
    gs = fig.add_gridspec(num_sub_plots, hspace=0)
    # axs = gs.subplots(sharex=True, sharey=True)
    axs = gs.subplots()
    # fig.suptitle("this is the super title")

    figsize = (8, 8)
    if num_sub_plots == 1:
        # df.plot(marker='.', figsize=figsize, ax=axs, color=get_column_color(df1))
        df[cols].plot(figsize=figsize, ax=axs)
        if show_y_lable:
            lable = cols.capitalize() if cols != "instances_num" else "Number of Instances"
            axs.set_ylabel(lable)
    if save_to:
        fpath = os.path.join(save_to, "job_" + cols + ".png")
        plt.savefig(fpath)
    else:
        plt.show()


def plot_stats_for_reward_signal(reward_type="", rename_col=True, use_cols=None, title=None, y_label=None):
    csv_path = get_exp_file_path(file_type=reward_type)
    df_stats = load_df(csv_path)
    # cols = ["reward_" + reward_type + "_" + avg_makespans, "reward_" + reward_type + "_" + avg_slowdowns,
    #         "reward_" + reward_type + "_" + avg_completions]
    cols = [avg_makespans, avg_slowdowns, avg_completions]
    if use_cols:
        cols = use_cols
    if rename_col:
        df = pd.DataFrame()
        for col in cols:
            df[col] = df_stats["reward_" + reward_type + "_" + col]
        df_stats = df.copy()
    plot_lines_from_df(df_stats[cols], title=title, y_label=y_label)


def plot_reward_avg_completions():
    plot_stats_for_reward_signal(reward_type=avg_completions, rename_col=True)


def plot_reward_avg_makespans():
    plot_stats_for_reward_signal(reward_type=avg_makespans, rename_col=True)


def plot_reward_avg_slowdowns():
    plot_stats_for_reward_signal(reward_type=avg_slowdowns, rename_col=True)


def plot_training_stats_for_reward_all():
    use_cols = [avg_completions]
    plot_stats_for_reward_signal(reward_type=avg_completions, rename_col=True, use_cols=use_cols,
                                 title=f"reward_{avg_completions}")
    plot_stats_for_reward_signal(reward_type=avg_makespans, rename_col=True, use_cols=use_cols,
                                 title=f"reward_{avg_makespans}")
    plot_stats_for_reward_signal(reward_type=avg_slowdowns, rename_col=True, use_cols=use_cols,
                                 title=f"reward_{avg_slowdowns}")


def plot_reward_data(dfs, cols=None):
    """
    plot avg_completion, avg_makespan, or avg_slowdown for different reward signals
    dfs contains a list of tuples, each tuple is of format (reward_type, df)
    this method plots one stat for multiple reward_types
    :param dfs:
    :param cols:
    :return:
    """
    if dfs:
        df_stats = pd.DataFrame()
        for reward_type, df in dfs:
            df_cols = df.columns.values.tolist()
            for col, curr_col in zip(cols, df_cols):
                if col and curr_col.endswith(col):
                    df_stats[reward_type] = df[curr_col]
        plot_lines_from_df(df_stats)


def plot_single_stat_for_all_reward_signals(dfs, col_name=None, y_label=None, curr_fig_dir=None, figsize=(10, 10),
                                            excludes=None, x_lable=None, ceiling=None, fig_name=None, ylim_low=None,
                                            ylim_high=None, logy=False):
    if dfs and col_name:
        df_stats = pd.DataFrame()
        for reward_type, df in dfs:
            cols = df.columns.values.tolist()
            for col in cols:
                if reward_type in other_algo_list and col_name == avg_makespans:
                    col_name = "env_now"
                if col and col.endswith(col_name):
                    if excludes and col in excludes:  # don't plot certain stats if specified
                        continue
                    df_stats[reward_type] = df[col]
        fig = plt.figure()
        num_sub_plots = 1
        gs = fig.add_gridspec(num_sub_plots, hspace=0)
        # axs = gs.subplots(sharex=True, sharey=True)
        axs = gs.subplots()
        # fig.suptitle("this is the super title")

        if not ceiling is None:
            df_stats = df_stats[df_stats[reward_type] < ceiling].copy()
        if y_label:
            axs.set_ylabel(y_label)
        if x_lable:
            axs.set_xlabel(xlabel=x_lable)
        if ylim_low and ylim_high:
            axs.set_ylim(ylim_low, ylim_high)

        if num_sub_plots == 1:
            # df.plot(marker='.', figsize=figsize, ax=axs, color=get_column_color(df1))
            df_stats.plot(marker='.', figsize=figsize, ax=axs, logy=logy)
        # for ax in axs:
        #     ax.label_outer()
        if curr_fig_dir:
            if fig_name is None:
                fig_name = "stats_" + col_name + ".png"
            figpath = os.path.join(curr_fig_dir, fig_name)
            plt.savefig(figpath)
        else:
            plt.show()


def plot_box_single_stat_for_all_reward_signals(dfs, col_name=None, y_label=None, curr_fig_dir=None, figsize=(10, 10),
                                                excludes=None, x_lable=None, ceiling=None, fig_name=None, ylim_low=None,
                                                ylim_high=None, logy=False):
    if dfs and col_name:
        df_stats = pd.DataFrame()
        for reward_type, df in dfs:
            cols = df.columns.values.tolist()
            for col in cols:
                if reward_type in other_algo_list and col_name == avg_makespans:
                    col_name = "env_now"
                if col and col.endswith(col_name):
                    if excludes and col in excludes:  # don't plot certain stats if specified
                        continue
                    df_stats[reward_type] = df[col]
        fig = plt.figure()
        num_sub_plots = 1
        gs = fig.add_gridspec(num_sub_plots, hspace=0)
        # axs = gs.subplots(sharex=True, sharey=True)
        axs = gs.subplots()
        # fig.suptitle("this is the super title")

        if not ceiling is None:
            df_stats = df_stats[df_stats[reward_type] < ceiling].copy()
        if y_label:
            axs.set_ylabel(y_label)
        if x_lable:
            axs.set_xlabel(xlabel=x_lable)
        if ylim_low and ylim_high:
            axs.set_ylim(ylim_low, ylim_high)

        if num_sub_plots == 1:
            # df.plot(marker='.', figsize=figsize, ax=axs, color=get_column_color(df1))
            df_stats.plot.box(figsize=figsize, ax=axs)
        # for ax in axs:
        #     ax.label_outer()
        if curr_fig_dir:
            if fig_name is None:
                fig_name = "stats_" + col_name + ".png"
            figpath = os.path.join(curr_fig_dir, fig_name)
            plt.savefig(figpath)
        else:
            plt.show()


def get_coloumn_name_ends_with(cols, suffix=None):
    if cols and suffix:
        name = [col for col in cols if col.endswith(suffix)]
        if name:
            # temp method for finding a matching name, names are unique so only one should be in the lsit
            return name[0]


def plot_box_stat_difference_for_all_reward_signals(dfs, compare_stat=None, reward_signal_name="", y_label=None,
                                                    curr_fig_dir=None,
                                                    figsize=(10, 10), excludes=None, df_compare_to=None,
                                                    compare_to_col_name="", suffix="", x_lable=None, ylim_low=None,
                                                    ylim_high=None):
    """
    this loops through each file and compare a specific stat (specified by the compare_stat) to the same
    stat trained for all other reward signals
    :param dfs:
    :param compare_stat:
    :param reward_signal_name:
    :param y_label:
    :param curr_fig_dir:
    :param figsize:
    :param excludes:
    :param df_compare_to:
    :return:
    """
    if dfs and compare_stat and not df_compare_to is None:
        df_stats = pd.DataFrame()
        for reward_type, df in dfs:
            cols = df.columns.values.tolist()
            for col in cols:
                if reward_type in other_algo_list and compare_stat == avg_makespans:
                    compare_stat = "env_now"
                if col and col.endswith(compare_stat):
                    if excludes and col in excludes:  # don't plot certain stats if specified
                        continue
                    # others minus the current stats to get the difference between performance
                    if reward_type in other_algo_list and col == avg_makespans:  # used a different name for other algo, so need to accomadate it
                        # col_name=reward_type + "_env_now"
                        df_stats[reward_type] = df[reward_type + "_env_now"] - df_compare_to[compare_to_col_name]
                    else:
                        curr_col = get_coloumn_name_ends_with(cols, suffix=compare_stat)
                        df_stats[reward_type] = df[curr_col] - df_compare_to[compare_to_col_name]
        fig = plt.figure()
        num_sub_plots = 1
        gs = fig.add_gridspec(num_sub_plots, hspace=0)
        # axs = gs.subplots(sharex=True, sharey=True)
        axs = gs.subplots()
        # fig.suptitle("this is the super title")

        if y_label:
            axs.set_ylabel(y_label)
        if x_lable:
            axs.set_xlabel(xlabel=x_lable)
        if ylim_low and ylim_high:
            axs.set_ylim(ylim_low, ylim_high)
        if num_sub_plots == 1:
            # df.plot(marker='.', figsize=figsize, ax=axs, color=get_column_color(df1))
            df_stats.plot.box(figsize=figsize, ax=axs)

        # for ax in axs:
        #     ax.label_outer()
        if curr_fig_dir:
            fname = reward_signal_name if reward_signal_name else compare_stat
            figpath = os.path.join(curr_fig_dir, "stat_diff_" + fname + suffix + ".png")
            plt.savefig(figpath)
        else:
            plt.show()


def plot_stat_difference_for_all_reward_signals(dfs, compare_stat=None, reward_signal_name="", y_label=None,
                                                curr_fig_dir=None,
                                                figsize=(10, 10), excludes=None, df_compare_to=None,
                                                compare_to_col_name="", suffix="", x_lable=None, ylim_low=None,
                                                ylim_high=None, logy=False, fig_name=None):
    """
    this loops through each file and compare a specific stat (specified by the compare_stat) to the same
    stat trained for all other reward signals
    :param dfs:
    :param compare_stat:
    :param reward_signal_name:
    :param y_label:
    :param curr_fig_dir:
    :param figsize:
    :param excludes:
    :param df_compare_to:
    :return:
    """
    if dfs and compare_stat and not df_compare_to is None:
        df_stats = pd.DataFrame()
        for reward_type, df in dfs:
            cols = df.columns.values.tolist()
            for col in cols:
                if reward_type in other_algo_list and compare_stat == avg_makespans:
                    compare_stat = "env_now"
                if col and col.endswith(compare_stat):
                    if excludes and col in excludes:  # don't plot certain stats if specified
                        continue
                    # others minus the current stats to get the difference between performance
                    if reward_type in other_algo_list and col == avg_makespans:  # used a different name for other algo, so need to accomadate it
                        # col_name=reward_type + "_env_now"
                        df_stats[reward_type] = df[reward_type + "_env_now"] - df_compare_to[compare_to_col_name]
                        # df_stats[reward_type] = df[reward_type + "_env_now"] - df_compare_to[compare_to_col_name]
                    else:
                        curr_col = get_coloumn_name_ends_with(cols, suffix=compare_stat)
                        df_stats[reward_type] = df[curr_col] - df_compare_to[compare_to_col_name]
                        # df_stats[reward_type] = df[curr_col] - df_compare_to[compare_to_col_name]
        fig = plt.figure()
        num_sub_plots = 1
        gs = fig.add_gridspec(num_sub_plots, hspace=0)
        # axs = gs.subplots(sharex=True, sharey=True)
        axs = gs.subplots()
        # fig.suptitle("this is the super title")

        if num_sub_plots == 1:
            # df.plot(marker='.', figsize=figsize, ax=axs, color=get_column_color(df1))
            df_stats.plot(marker='.', figsize=figsize, ax=axs, logy=logy)
        if y_label:
            axs.set_ylabel(y_label)
        if x_lable:
            axs.set_xlabel(xlabel=x_lable)
        if ylim_low and ylim_high:
            axs.set_ylim(ylim_low, ylim_high)

        # for ax in axs:
        #     ax.label_outer()
        if curr_fig_dir:
            if fig_name is None:
                fname = reward_signal_name if reward_signal_name else compare_stat
                fig_name = "stat_diff_" + fname + suffix + ".png"
            figpath = os.path.join(curr_fig_dir, fig_name)
            plt.savefig(figpath)
        else:
            plt.show()


# @exp_fig
def exp_results_by_reward_all_plots():
    """
    this plots avg_completions, avg_makespans, avg_slowdowns for all reward signals
    :return:
    """
    # if fig dir is specified, the figs will be save to the dir
    # curr_fig_dir = "/Users/jackz/Documents/P_Macbook/Laptop/Git_Workspace/DataScience/MachineLearning/MyForks/CloudSimPy/experiments/figs/by_reward/all_stat"
    df_completion = load_df(get_exp_file_path(file_type=RAC))
    df_makespan = load_df(get_exp_file_path(file_type=RAM))
    df_slowdown = load_df(get_exp_file_path(file_type=RAS))
    df_mix_acas = load_df(get_exp_file_path(file_type=MIX_AC_AS))
    # df_others = load_df(get_exp_file_path(file_type=other_algo))
    df_tetris = load_df(get_exp_file_path(file_type=algo_tetris))
    df_random = load_df(get_exp_file_path(file_type=algo_random))
    df_first_fit = load_df(get_exp_file_path(file_type=algo_first_fit))
    range = None
    figname_prefix = "RAC_"
    curr_fig_dir = "experiments/figs/by_reward/comparisons"
    # curr_fig_dir="experiments/figs/by_reward/comparisons/with_random"
    curr_fig_dir = "experiments/figs/by_reward/comparisons/all_rewards"
    if range is None:
        dfs = [(RAC, df_completion), (RAM, df_makespan), (RAS, df_slowdown), (MIX_AC_AS, df_mix_acas),
               (algo_random, df_random),
               (algo_first_fit, df_first_fit),
               (algo_tetris, df_tetris)]
        dfs = [(RAC, df_completion), (RAM, df_makespan), (RAS, df_slowdown), (MIX_AC_AS, df_mix_acas)]
        dfs = [
            # (RAM, df_makespan),
            (RAC, df_completion),
            # (RAS, df_slowdown),
            # (MIX_AC_AS, df_mix_acas),
            (algo_random, df_random),
            (algo_first_fit, df_first_fit),
            (algo_tetris, df_tetris)
        ]
    else:
        dfs = [(RAC, df_completion[:range]), (RAM, df_makespan[:range]), (RAS, df_slowdown[:range]),
               (MIX_AC_AS, df_mix_acas[:range])]
        dfs = [(RAC, df_completion[:range]), (RAM, df_makespan[:range]), (RAS, df_slowdown[:range]),
               (MIX_AC_AS, df_mix_acas[:range]),
               (algo_random, df_random[:range]),
               (algo_first_fit, df_first_fit[:range]),
               (algo_tetris, df_tetris[:range])]
        dfs = [
            # (RAM, df_makespan[:range]),
            #    (RAC, df_completion[:range]),
            # (RAS, df_slowdown[:range]),
            # (MIX_AC_AS, df_mix_acas[:range]),
            (algo_random, df_random[:range]),
            # (algo_first_fit, df_first_fit[:range]),
            # (algo_tetris, df_tetris[:range])
        ]
    excludes = []
    y1 = 0
    y2 = 100

    log_y = True
    # avg completions data using different training reward
    plot_single_stat_for_all_reward_signals(dfs, col_name=avg_completions, y_label="Average Completions",
                                            curr_fig_dir=curr_fig_dir, x_lable="Job Chunk Number", ceiling=None,
                                            ylim_low=y1, ylim_high=y2, logy=log_y,
                                            fig_name=figname_prefix + "_completions.png")
    # avg makespans data using different training reward
    plot_single_stat_for_all_reward_signals(dfs, col_name=avg_makespans, y_label="Average Makespans",
                                            curr_fig_dir=curr_fig_dir, ceiling=None,
                                            x_lable="Job Chunk Number", ylim_low=y1, ylim_high=y2, logy=log_y,
                                            fig_name=figname_prefix + "_makespans.png")
    # avg slowdosns data using different training reward
    plot_single_stat_for_all_reward_signals(dfs, col_name=avg_slowdowns, y_label="Average Slowdowns",
                                            curr_fig_dir=curr_fig_dir, ceiling=None,
                                            x_lable="Job Chunk Number", ylim_low=y1, ylim_high=y2, logy=log_y,
                                            fig_name=figname_prefix + "_slowdowns.png")
    # plot_box_single_stat_for_all_reward_signals(dfs, col_name=avg_completions, y_label="Average Makespans",
    #                                             curr_fig_dir=curr_fig_dir, ceiling=None,
    #                                             x_lable="Job Chunk Number")


def get_all_stats_df_old(range=0, exclude=None):
    df_completion = load_df(get_exp_file_path(file_type=avg_completions))
    df_makespan = load_df(get_exp_file_path(file_type=avg_makespans))
    df_slowdown = load_df(get_exp_file_path(file_type=avg_slowdowns))
    # df_others = load_df(get_exp_file_path(file_type=other_algo))
    df_tetris = load_df(get_exp_file_path(file_type=algo_tetris))
    df_random = load_df(get_exp_file_path(file_type=algo_random))
    df_first_fit = load_df(get_exp_file_path(file_type=algo_first_fit))
    if range > 0:
        return df_completion[:range], df_makespan[:range], df_slowdown[:range], \
               df_tetris[:range], df_random[:range], df_first_fit[:range]
    else:
        return df_completion, df_makespan, df_slowdown, df_tetris, df_random, df_first_fit


def get_all_stats_df(range=0, exclude=None):
    df_completion = load_df(get_exp_file_path(file_type=RAC))
    df_makespan = load_df(get_exp_file_path(file_type=RAM))
    df_slowdown = load_df(get_exp_file_path(file_type=RAS))
    df_mix_acas = load_df(get_exp_file_path(file_type=MIX_AC_AS))
    # df_others = load_df(get_exp_file_path(file_type=other_algo))
    df_tetris = load_df(get_exp_file_path(file_type=algo_tetris))
    df_random = load_df(get_exp_file_path(file_type=algo_random))
    df_first_fit = load_df(get_exp_file_path(file_type=algo_first_fit))
    if range > 0:
        return df_completion[:range], df_makespan[:range], df_slowdown[:range], df_mix_acas[:range], \
               df_tetris[:range], df_random[:range], df_first_fit[:range]
    else:
        return df_completion, df_makespan, df_slowdown, df_mix_acas, df_tetris, df_random, df_first_fit


# @exp_fig
def exp_stats_diff_by_reward_all_plots():
    """
    this plots the difference between two stats
    :return:
    """
    # if fig dir is specified, the figs will be save to the dir
    # curr_fig_dir = "/Users/jackz/Documents/P_Macbook/Laptop/Git_Workspace/DataScience/MachineLearning/MyForks/CloudSimPy/experiments/figs/stats_diff"
    # curr_fig_dir = None
    range = None
    if range is None:
        df_completion, df_makespan, df_slowdown, df_mix_acas, df_tetris, df_random, df_first_fit = get_all_stats_df()
    else:
        df_completion, df_makespan, df_slowdown, df_mix_acas, df_tetris, df_random, df_first_fit = get_all_stats_df(
            range=180)

    # dfs = [(RAC, df_completion), (RAM, df_makespan), (RAS, df_slowdown), (algo_random, df_random),
    #        (algo_first_fit, df_first_fit),
    #        (algo_tetris, df_tetris)]
    dfs_makespans = [(RAC, df_completion), (RAS, df_slowdown), (MIX_AC_AS, df_mix_acas), (algo_random, df_random),
                     (algo_first_fit, df_first_fit),
                     (algo_tetris, df_tetris)]
    dfs_completions = [(RAM, df_makespan), (RAS, df_slowdown), (MIX_AC_AS, df_mix_acas), (algo_random, df_random),
                       (algo_first_fit, df_first_fit),
                       (algo_tetris, df_tetris)]
    dfs_slowdowns = [(RAC, df_completion), (RAM, df_makespan), (MIX_AC_AS, df_mix_acas), (algo_random, df_random),
                     (algo_first_fit, df_first_fit),
                     (algo_tetris, df_tetris)]
    dfs_mix_acas = [(RAM, df_makespan), (RAC, df_completion), (RAM, df_makespan), (algo_random, df_random),
                    (algo_first_fit, df_first_fit),
                    (algo_tetris, df_tetris)]

    excludes = []
    suffix = ""
    curr_fig_dir = None
    # avg completions data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_completions, compare_stat=avg_completions,
                                                y_label="Average Completions Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_completion,
                                                compare_to_col_name=f"{reward_avg_completions}_{avg_completions}",
                                                suffix=suffix, x_lable="Job Chunk Number")
    # avg makespans data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_makespans, compare_stat=avg_makespans,
                                                y_label="Average Makespans Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_makespan,
                                                compare_to_col_name=f"{reward_avg_makespans}_{avg_makespans}",
                                                suffix=suffix, x_lable="Job Chunk Number")
    # # avg slowdosns data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_slowdowns, compare_stat=avg_slowdowns,
                                                y_label="Average Slowdowns Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_slowdown,
                                                compare_to_col_name=f"{reward_avg_slowdowns}_{avg_slowdowns}",
                                                suffix=suffix, x_lable="Job Chunk Number")
    # # # mix acas data using different training reward
    # plot_stat_difference_for_all_reward_signals(dfs_mix_acas, compare_stat=MIX_AC_AS,
    #                                             y_label="Average Slowdowns Difference",
    #                                             curr_fig_dir=curr_fig_dir, df_compare_to=df_mix_acas,
    #                                             compare_to_col_name=f"{MIX_AC_AS}_{avg_mix_acas}",
    #                                             suffix=suffix, x_lable="Job Chunk Number")


# @exp_fig
def exp_stats_diff_by_reward_single_reward_comparison_all_plots():
    """
    this plots the difference between a single reward and other algorithms
    :return:
    """
    # if fig dir is specified, the figs will be save to the dir
    # curr_fig_dir = "/Users/jackz/Documents/P_Macbook/Laptop/Git_Workspace/DataScience/MachineLearning/MyForks/CloudSimPy/experiments/figs/stats_diff"
    # curr_fig_dir = None
    range = None
    if range is None:
        df_completion, df_makespan, df_slowdown, df_mix_acas, df_tetris, df_random, df_first_fit = get_all_stats_df()
    else:
        df_completion, df_makespan, df_slowdown, df_mix_acas, df_tetris, df_random, df_first_fit = get_all_stats_df(
            range=180)

    # dfs = [(RAC, df_completion), (RAM, df_makespan), (RAS, df_slowdown), (algo_random, df_random),
    #        (algo_first_fit, df_first_fit),
    #        (algo_tetris, df_tetris)]

    dfs_other_algo = [
        # (RAC, df_completion),
        # (RAM, df_makespan),
        # (MIX_AC_AS, df_mix_acas),
        # (RAS, df_slowdown),
        # (algo_random, df_random),
        (algo_first_fit, df_first_fit),
        (algo_tetris, df_tetris)]
    # dfs_makespans = [
    #     # (algo_random, df_random),
    #     # (algo_first_fit, df_first_fit),
    #     (algo_tetris, df_tetris)]
    # dfs_completions = [
    #     # (algo_random, df_random),
    #     (algo_first_fit, df_first_fit),
    #     (algo_tetris, df_tetris)]
    # dfs_slowdowns = [
    #     # (algo_random, df_random),
    #     (algo_first_fit, df_first_fit),
    #     (algo_tetris, df_tetris)]

    excludes = []
    # suffix = ""
    # curr_fig_dir = "experiments/figs/stats_diff"
    curr_fig_dir = None
    # suffix=f"{RAM}_"
    df_compare = df_makespan
    curr_reward = reward_avg_makespans
    logy = False
    # avg completions data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_other_algo, compare_stat=avg_completions,
                                                y_label="Average Completions Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_compare,
                                                compare_to_col_name=f"{curr_reward}_{avg_completions}",
                                                suffix="_completions", x_lable="Job Chunk Number", logy=logy)
    # avg makespans data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_other_algo, compare_stat=avg_makespans,
                                                y_label="Average Makespans Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_compare,
                                                compare_to_col_name=f"{curr_reward}_{avg_makespans}",
                                                suffix="_makespans", x_lable="Job Chunk Number", logy=logy)
    # # avg slowdosns data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_other_algo, compare_stat=avg_slowdowns,
                                                y_label="Average Slowdowns Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_compare,
                                                compare_to_col_name=f"{curr_reward}_{avg_slowdowns}",
                                                suffix="_slowdowns", x_lable="Job Chunk Number", logy=logy)


def get_job_stats(all_in_one_chart=False):
    df_jobs = load_df(job_file_path)
    save_dir = "/Users/jackz/Documents/P_Macbook/Laptop/Git_Workspace/DataScience/MachineLearning/MyForks/CloudSimPy/experiments/figs/job_stats"
    cols = ['duration', 'memory', 'instances_num']
    plot_all_job_stats_from_df(df_jobs, cols=cols, save_to=save_dir)  # this plots all stats in one chart
    # for col in cols:
    #     plot_individual_job_stats_from_df(df_jobs, cols=col, save_to=save_dir)


def get_df_corr(df, result=None, data_type="", corrtype="pearson", compare_to="", idx_col="Unnamed: 0",
                return_all=False, sort_corr=False):
    if not result is None and not df is None:
        corr_matrix = df.corr(method=corrtype)
        col_name = f"{data_type}_{corrtype}"
        if sort_corr:
            corr_matrix = corr_matrix.sort_index().copy()
        if return_all:
            return corr_matrix
        else:
            result[col_name] = corr_matrix[compare_to]
            return result


def collect_df_corrs(dfs=None):
    corrtype = "pearson"
    stat_name = avg_makespans
    reward_type = RAM
    df_all = get_all_stats_df()
    df_corr = pd.DataFrame()
    for df in df_all:
        cols = df.columns.values.tolist()
        curr_cols = [col for col in cols if col.endswith(stat_name) and col]
        df_corr[curr_cols] = df[curr_cols]
    corr_matrix = df_corr.corr(method=corrtype)
    print(corr_matrix)


# @exp_fig
def temp_exp_results_by_reward_all_plots():
    """
    this plots avg_completions, avg_makespans, avg_slowdowns for all reward signals
    :return:
    """
    # if fig dir is specified, the figs will be save to the dir
    # curr_fig_dir = "/Users/jackz/Documents/P_Macbook/Laptop/Git_Workspace/DataScience/MachineLearning/MyForks/CloudSimPy/experiments/figs/by_reward/all_stat"
    path_big = "experiments/data/temp/hist_RAM_big.csv"
    path_my = "experiments/data/temp/hist_RAM_my.csv"
    df_big = load_df(path_big)
    df_my = load_df(path_my)

    # df_ram_mybrain =

    df_train_ram_big = load_df("curr_agents/RAM_Big/hist_deepjs_train_RAM_0.csv")
    df_train_ram_mybrain = load_df("curr_agents/RAM_MyBrain/hist_deepjs_train_RAM_0.csv")
    df_train_old = load_df("data/old_data2/train_stats/hist_RAM_deepjs.csv")
    df_train_rac_old = load_df("data/old_data2/train_stats/hist_RAC_deepjs.csv")
    df_train_rac_mybrain = load_df("experiments/data/temp/rac_mybrain/hist_deepjs_train_RAC_0.csv")
    df_train_ras_old = load_df("data/old_data2/train_stats/hist_RAS_deepjs.csv")
    df_eval_rac_dill = load_df("experiments/data/eval/temp_eval/hist_ram_dill_.csv")
    df_eval_rac_my50 = load_df("experiments/data/eval/temp_eval/hist_RAC_My50_.csv")

    df_tetris = load_df("experiments/data/eval/hist_tetris.csv")
    df_random = load_df("experiments/data/eval/hist_random.csv")
    df_first_fit = load_df("experiments/data/eval/hist_first_fit.csv")
    range = None
    figname_prefix = "RAC_dill_eval_"
    curr_fig_dir = "experiments/figs/by_reward/comparisons"
    # curr_fig_dir="experiments/figs/by_reward/comparisons/with_random"
    # curr_fig_dir = "experiments/figs/by_reward/comparisons/all_rewards"
    curr_fig_dir = "experiments/data/eval/temp_figs"
    if range is None:
        # dfs = [(RAC, df_completion), (RAM, df_makespan), (RAS, df_slowdown), (MIX_AC_AS, df_mix_acas),
        #        (algo_random, df_random),
        #        (algo_first_fit, df_first_fit),
        #        (algo_tetris, df_tetris)]
        # dfs = [(RAC, df_completion), (RAM, df_makespan), (RAS, df_slowdown), (MIX_AC_AS, df_mix_acas)]
        dfs = [
            # (RAM, df_makespan),
            # ("RAM_Big", df_train_ram_big),
            # ("RAM_my", df_train_ram_mybrain),
            # ("RAM_old", df_train_old),
            # ("RAC_old", df_train_rac_old),
            # ("RAC_mybrain", df_train_rac_mybrain),
            # ("RAS_old", df_train_ras_old),
            ("RAC_dill", df_eval_rac_dill),
            # ("RAC_My50", df_eval_rac_my50),

            # (RAS, df_slowdown),
            # (MIX_AC_AS, df_mix_acas),
            # (algo_random, df_random),
            (algo_first_fit, df_first_fit),
            (algo_tetris, df_tetris)
        ]
    excludes = []
    y1 = 0
    y2 = 100

    log_y = False
    # avg completions data using different training reward
    plot_single_stat_for_all_reward_signals(dfs, col_name=avg_completions, y_label="Average Completions",
                                            curr_fig_dir=curr_fig_dir, x_lable="Job Chunk Number", ceiling=None,
                                            ylim_low=y1, ylim_high=y2, logy=log_y,
                                            fig_name=figname_prefix + "_completions.png")
    # avg makespans data using different training reward
    plot_single_stat_for_all_reward_signals(dfs, col_name=avg_makespans, y_label="Average Makespans",
                                            curr_fig_dir=curr_fig_dir, ceiling=None,
                                            x_lable="Job Chunk Number", ylim_low=y1, ylim_high=y2, logy=log_y,
                                            fig_name=figname_prefix + "_makespans.png")
    # avg slowdosns data using different training reward
    plot_single_stat_for_all_reward_signals(dfs, col_name=avg_slowdowns, y_label="Average Slowdowns",
                                            curr_fig_dir=curr_fig_dir, ceiling=None,
                                            x_lable="Job Chunk Number", ylim_low=y1, ylim_high=y2, logy=log_y,
                                            fig_name=figname_prefix + "_slowdowns.png")


# @exp_fig
def temp_exp_stats_diff_by_reward_single_reward_comparison_all_plots():
    """
    this plots the difference between a single reward and other algorithms
    :return:
    """
    # if fig dir is specified, the figs will be save to the dir
    # curr_fig_dir = "/Users/jackz/Documents/P_Macbook/Laptop/Git_Workspace/DataScience/MachineLearning/MyForks/CloudSimPy/experiments/figs/stats_diff"
    # curr_fig_dir = None
    range = 320
    df_eval_rac_dill = load_df("experiments/data/eval/temp_eval/hist_ram_dill_.csv")[:range].copy()
    df_eval_rac_my50 = load_df("experiments/data/eval/temp_eval/hist_RAC_My50_.csv")[:range].copy()

    df_tetris = load_df("experiments/data/eval/hist_tetris.csv")[:range].copy()
    df_random = load_df("experiments/data/eval/hist_random.csv")[:range].copy()
    df_first_fit = load_df("experiments/data/eval/hist_first_fit.csv")[:range].copy()
    # if range is None:
    #     df_completion, \
    #     df_makespan, \
    #     df_slowdown, \
    #     df_mix_acas, \
    #     df_tetris, df_random, df_first_fit = get_all_stats_df()
    # else:
    #     df_completion, df_makespan, df_slowdown, df_mix_acas, df_tetris, df_random, df_first_fit = get_all_stats_df(
    #         range=180)

    # dfs = [(RAC, df_completion), (RAM, df_makespan), (RAS, df_slowdown), (algo_random, df_random),
    #        (algo_first_fit, df_first_fit),
    #        (algo_tetris, df_tetris)]

    dfs_other_algo = [
        # (RAC, df_completion),
        # (RAM, df_makespan),
        # (MIX_AC_AS, df_mix_acas),
        # (RAS, df_slowdown),
        # (algo_random, df_random),
        (algo_first_fit, df_first_fit),
        (algo_tetris, df_tetris)
    ]
    # dfs_makespans = [
    #     # (algo_random, df_random),
    #     # (algo_first_fit, df_first_fit),
    #     (algo_tetris, df_tetris)]
    # dfs_completions = [
    #     # (algo_random, df_random),
    #     (algo_first_fit, df_first_fit),
    #     (algo_tetris, df_tetris)]
    # dfs_slowdowns = [
    #     # (algo_random, df_random),
    #     (algo_first_fit, df_first_fit),
    #     (algo_tetris, df_tetris)]

    excludes = []
    # suffix = ""
    # curr_fig_dir = "experiments/figs/stats_diff"
    curr_fig_dir = "experiments/data/eval/temp_figs"
    # suffix=f"{RAM}_"
    df_compare = df_eval_rac_my50[:range].copy()
    df_compare = df_eval_rac_dill[:range].copy()
    curr_reward = "ram_dill_"
    # curr_reward = "RAC_My50_"
    logy = False
    # avg completions data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_other_algo, compare_stat=avg_completions,
                                                y_label="Average Completions Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_compare,
                                                compare_to_col_name=f"{curr_reward}_{avg_completions}",
                                                suffix="_completions", x_lable="Job Chunk Number", logy=logy)
    # avg makespans data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_other_algo, compare_stat=avg_makespans,
                                                y_label="Average Makespans Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_compare,
                                                compare_to_col_name=f"{curr_reward}_{avg_makespans}",
                                                suffix="_makespans", x_lable="Job Chunk Number", logy=logy)
    # # avg slowdosns data using different training reward
    plot_stat_difference_for_all_reward_signals(dfs_other_algo, compare_stat=avg_slowdowns,
                                                y_label="Average Slowdowns Difference",
                                                curr_fig_dir=curr_fig_dir, df_compare_to=df_compare,
                                                compare_to_col_name=f"{curr_reward}_{avg_slowdowns}",
                                                suffix="_slowdowns", x_lable="Job Chunk Number", logy=logy)


def count_stats():
    df_eval_rac_dill = load_df("experiments/data/eval/temp_eval/hist_ram_dill_.csv")
    df_eval_rac_my50 = load_df("experiments/data/eval/temp_eval/hist_RAC_My50_.csv")
    df_tetris = load_df("experiments/data/eval/hist_tetris.csv")
    df_random = load_df("experiments/data/eval/hist_random.csv")
    df_first_fit = load_df("experiments/data/eval/hist_first_fit.csv")
    range = -1
    if range > 0:
        df_compare = df_eval_rac_dill[:range].copy()
        df_compare = df_eval_rac_my50[:range].copy()
        dfs = [
            df_random[:range].copy(),
            df_tetris[:range].copy(), df_first_fit[:range].copy()]
    else:
        df_compare = df_eval_rac_dill
        df_compare = df_eval_rac_my50
        dfs = [
            df_random,
            df_tetris, df_first_fit]
    curr_reward = "ram_dill__"
    curr_reward = "RAC_My50__"
    count_dict = defaultdict(list)
    metrics = [avg_makespans, avg_completions, avg_slowdowns]

    for metric in metrics:
        for df_curr in dfs:
            cols = df_curr.columns.values.tolist()
            curr_col = [curr_col for curr_col in cols if curr_col.endswith(metric)][0]
            df_bigger = df_curr[df_curr[curr_col] > df_compare[curr_reward + metric]]
            df_smaller = df_curr[df_curr[curr_col] < df_compare[curr_reward + metric]]
            df_eq = df_curr[df_curr[curr_col] == df_compare[curr_reward + metric]]
            count_dict[curr_col + "_bigger"].append(len(df_bigger))
            count_dict[curr_col + "_smaller"].append(len(df_smaller))
            count_dict[curr_col + "_eq"].append(len(df_eq))
            # percent
            count_dict[curr_col + "_bigger"].append(len(df_bigger) / len(df_curr))
            count_dict[curr_col + "_smaller"].append(len(df_smaller) / len(df_curr))
            count_dict[curr_col + "_eq"].append(len(df_eq) / len(df_curr))

    print(count_dict)


if __name__ == '__main__':
    # plot_avg_slowdown()
    # exp_results_by_reward_all_plots()
    # plot_reward_avg_completions()
    # plot_reward_avg_slowdowns()
    # rename_add_reward_type()
    # plot_training_stats_for_reward_all()
    # exp_results_by_reward_all_plots()
    # get_job_stats()
    # exp_stats_diff_by_reward_all_plots()
    # temp_exp_results_by_reward_all_plots()
    # temp_exp_stats_diff_by_reward_single_reward_comparison_all_plots()
    count_stats()
    # exp_results_by_reward_all_plots()
    # collect_df_corrs()

# brain RAC dill 200
{'random_avg_makespans_bigger': [142, 0.44375], 'random_avg_makespans_smaller': [110, 0.34375],
 'random_avg_makespans_eq': [68, 0.2125],
 'tetris_avg_makespans_bigger': [202, 0.63125],
 'tetris_avg_makespans_smaller': [85, 0.265625], 'tetris_avg_makespans_eq': [33, 0.103125],
 'first_fit_avg_makespans_bigger': [211, 0.659375], 'first_fit_avg_makespans_smaller': [79, 0.246875],
 'first_fit_avg_makespans_eq': [30, 0.09375], 'random_avg_completions_bigger': [143, 0.446875],
 'random_avg_completions_smaller': [168, 0.525], 'random_avg_completions_eq': [9, 0.028125],
 'tetris_avg_completions_bigger': [50, 0.15625], 'tetris_avg_completions_smaller': [265, 0.828125],
 'tetris_avg_completions_eq': [5, 0.015625], 'first_fit_avg_completions_bigger': [13, 0.040625],
 'first_fit_avg_completions_smaller': [302, 0.94375], 'first_fit_avg_completions_eq': [5, 0.015625],
 'random_avg_slowdowns_bigger': [166, 0.51875], 'random_avg_slowdowns_smaller': [147, 0.459375],
 'random_avg_slowdowns_eq': [7, 0.021875], 'tetris_avg_slowdowns_bigger': [69, 0.215625],
 'tetris_avg_slowdowns_smaller': [246, 0.76875], 'tetris_avg_slowdowns_eq': [5, 0.015625],
 'first_fit_avg_slowdowns_bigger': [27, 0.084375], 'first_fit_avg_slowdowns_smaller': [289, 0.903125],
 'first_fit_avg_slowdowns_eq': [4, 0.0125]}

### RAC MyBrain 50 trained
{'random_avg_makespans_bigger': [138, 0.43125], 'random_avg_makespans_smaller': [114, 0.35625],
 'random_avg_makespans_eq': [68, 0.2125], 'tetris_avg_makespans_bigger': [204, 0.6375],
 'tetris_avg_makespans_smaller': [81, 0.253125], 'tetris_avg_makespans_eq': [35, 0.109375],
 'first_fit_avg_makespans_bigger': [208, 0.65], 'first_fit_avg_makespans_smaller': [79, 0.246875],
 'first_fit_avg_makespans_eq': [33, 0.103125], 'random_avg_completions_bigger': [141, 0.440625],
 'random_avg_completions_smaller': [170, 0.53125], 'random_avg_completions_eq': [9, 0.028125],
 'tetris_avg_completions_bigger': [51, 0.159375], 'tetris_avg_completions_smaller': [264, 0.825],
 'tetris_avg_completions_eq': [5, 0.015625], 'first_fit_avg_completions_bigger': [12, 0.0375],
 'first_fit_avg_completions_smaller': [303, 0.946875], 'first_fit_avg_completions_eq': [5, 0.015625],
 'random_avg_slowdowns_bigger': [168, 0.525], 'random_avg_slowdowns_smaller': [145, 0.453125],
 'random_avg_slowdowns_eq': [7, 0.021875], 'tetris_avg_slowdowns_bigger': [71, 0.221875],
 'tetris_avg_slowdowns_smaller': [244, 0.7625], 'tetris_avg_slowdowns_eq': [5, 0.015625],
 'first_fit_avg_slowdowns_bigger': [26, 0.08125], 'first_fit_avg_slowdowns_smaller': [290, 0.90625],
 'first_fit_avg_slowdowns_eq': [4, 0.0125]}