#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstring>

// Structure to hold player data incoming from Python
struct Player {
    char name[50];
    char position[20];
    char team[30];
    int cost;
    double form_rating; 
    int historical_points;
};

// Global vector to hold results back to Python
std::vector<Player> optimal_lineup;

extern "C" {
    // 1. Predictive Engine: Analyzes form and history to project match-day points
    double calculate_predicted_points(double form, int history) {
        return (form * 0.7) + (static_cast<double>(history) * 0.3);
    }

    // 2. Optimization Engine: Multi-constraint 0/1 Knapsack
    void optimize_lineup(Player* players, int count, int max_budget, int max_per_team) {
        optimal_lineup.clear();
        
        std::vector<double> predicted_values(count);
        for(int i = 0; i < count; ++i) {
            predicted_values[i] = calculate_predicted_points(players[i].form_rating, players[i].historical_points);
        }

        // DP Table
        std::vector<std::vector<double>> dp(count + 1, std::vector<double>(max_budget + 1, 0.0));

        for (int i = 1; i <= count; ++i) {
            int current_cost = players[i - 1].cost;
            double current_val = predicted_values[i - 1];

            for (int w = 0; w <= max_budget; ++w) {
                if (current_cost <= w) {
                    dp[i][w] = std::max(dp[i - 1][w], dp[i - 1][w - current_cost] + current_val);
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        // Backtracking
        int w = max_budget;
        for (int i = count; i > 0 && w > 0; --i) {
            if (dp[i][w] != dp[i - 1][w]) {
                optimal_lineup.push_back(players[i - 1]);
                w -= players[i - 1].cost;
            }
        }
    }

    // Helpers for Python to grab data
    int get_optimal_count() {
        return optimal_lineup.size();
    }

    void get_optimal_player(int index, Player* out_player) {
        if (index >= 0 && index < static_cast<int>(optimal_lineup.size())) {
            std::strcpy(out_player->name, optimal_lineup[index].name);
            std::strcpy(out_player->position, optimal_lineup[index].position);
            std::strcpy(out_player->team, optimal_lineup[index].team);
            out_player->cost = optimal_lineup[index].cost;
            out_player->form_rating = optimal_lineup[index].form_rating;
            out_player->historical_points = optimal_lineup[index].historical_points;
        }
    }
}
