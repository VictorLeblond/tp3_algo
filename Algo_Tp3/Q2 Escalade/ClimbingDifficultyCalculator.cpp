// Nom, Matricule
// Nom, Matricule

#include "ClimbingDifficultyCalculator.h"
#include <fstream>
#include <sstream>
#include <vector>
#include <iterator>
#include <set>
// #include <math.h>
#include <algorithm>
#include <iostream>
using namespace std;
// ce fichier contient les definitions des methodes de la classe ClimbingDifficultyCalculator
// this file contains the definitions of the methods of the ClimbingDifficultyCalculator class

ClimbingDifficultyCalculator::ClimbingDifficultyCalculator()
{
}
int ClimbingDifficultyCalculator::CalculateClimbingDifficulty(std::string filename)
{
    int totalCost = numeric_limits<int>::max();
    vector<vector<int>> wall;
    string s;
    ifstream file;
    file.open(filename);

    while (getline(file, s))
    {
        istringstream iss(s);
        vector<int> cL;
        string w;
        char delim = ',';

        while (getline(iss, w, delim))
        {
            cL.push_back(stoi(w));
        }
        wall.push_back(cL);
    }
    file.close();

    vector<vector<int>> matrix(wall.size() + 1, vector<int>(wall[0].size() + 2, 0));
    for (int i = 0; i < wall.size() + 1; i++)
    {
        for (int j = 0; j < wall[0].size() + 2; j++)
        {
            if (j > wall[0].size() + 1)
                break;
            if (i == 0)
            {
                matrix[i][j] = 0;
            }
            else if (j == 0 || j == wall[0].size() + 1)
            {
                matrix[i][j] = numeric_limits<int>::max();
            }
            else if (i == 1)
            {
                matrix[i][j] = wall[wall.size() - i][j - 1];
            }
            else
            {
                set<int> possiblePath;
                for (int k = 1; k <= wall[0].size(); k++)
                {
                    int value = matrix[i - 1][k];
                    for (int v = min(j, k); v < max(j, k); v++)
                    {
                        if (j != k)
                            value += wall[wall.size() - i][(j < k) ? v : v - 1];
                    }
                    possiblePath.insert(value);
                }

                matrix[i][j] = wall[wall.size() - i][j - 1] + *possiblePath.begin();
            }
            //cout << matrix[i][j] << "\t";
        }

        //cout << endl;
    }

    return *min_element(matrix[wall.size()].begin(),matrix[wall.size()].end());
}