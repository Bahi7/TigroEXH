#pragma once
#include "Lat.h"
#include <nlohmann/json.hpp>

namespace fs = std::filesystem;
using json = nlohmann::json;

std::string input_directory = "MM\\MM";

double calculateExpectedValueSquared(const std::unordered_map<std::string, std::vector<std::string>>& myMap) {
    double sumOfSquares = 0.0;
    int numberOfKeys = 0;

    for (const auto& pair : myMap) {
        int length = pair.second.size();  // Length of the vector for this key
        sumOfSquares += length * length;  // Add the square of the length
        numberOfKeys++;
    }

    if (numberOfKeys == 0) return 0;  // Avoid division by zero

    return sumOfSquares / numberOfKeys;  // Calculate the average of the squares
}



// Function to reverse the map
std::unordered_map<std::string, std::vector<std::string>> reverseMap(
    const json& originalMap) {

    std::unordered_map<std::string, std::vector<std::string>> reversedMap;
    for (auto& [key, value] : originalMap.items()) {
        for (const auto& str : value) {
            reversedMap[str].push_back(key);
        }
    }
    return reversedMap;
}

// Function to reverse the map back
std::unordered_map<std::string, std::vector<std::string>> reverseMapBack(
    const std::unordered_map<std::string, std::vector<std::string>>& reversedMap) {

    std::unordered_map<std::string, std::vector<std::string>> originalMap;
    for (const auto& pair : reversedMap) {
        for (const auto& str : pair.second) {
            originalMap[str].push_back(pair.first);
        }
    }
    return originalMap;
}
static std::unordered_map<std::string, std::vector<std::string>> readAndMergeJSONFiles(const std::string& directory, size_t size_of_data) {
    std::cout << "Reading MM..." << std::endl;

    std::unordered_map<std::string, std::vector<std::string>> dataMap;
    size_t maxValues = 0;  // To track the maximum number of values for a single key
    size_t totalPairs = 0; // To track the total number of key-value pairs

    for (const auto& entry : fs::directory_iterator(directory)) {
        if (totalPairs >= size_of_data) {
            break;  // Stop if we have reached the size limit
        }

        if (entry.path().extension() == ".json") {
            std::ifstream file(entry.path());
            if (!file.is_open()) {
                std::cerr << "Failed to open " << entry.path() << std::endl;
                continue;
            }

            json j;
            file >> j;
            file.close();
            auto revMap = reverseMap(j);

            // Update the unordered_map
            for (const auto& pair : revMap) {

                for (const auto& item : pair.second) {

                    dataMap[pair.first].push_back(item);
                    totalPairs++;
                    maxValues = std::max(maxValues, dataMap[pair.first].size());
                    if (totalPairs >= size_of_data) {

                        return reverseMapBack(dataMap);  // Return the map if size limit is reached
                    }
                }
            }
        }
    }

    return reverseMapBack(dataMap);
}

int printStatistics(const std::unordered_map<std::string, std::vector<std::string>>* dataMap) {
    if (dataMap->empty()) {
        std::cout << "The map is empty." << std::endl;
        return 0;
    }

    size_t maxValues = 0;
    size_t totalPairs = 0;
    double sumOfSquares = 0.0;

    for (const auto& pair : *dataMap) {
        maxValues = std::max(maxValues, pair.second.size());
        totalPairs += pair.second.size();
        sumOfSquares += std::pow(pair.second.size(), 2);
    }

    double expectedValueSquared = sumOfSquares / dataMap->size();

    std::cout << "Maximum values for a key: " << maxValues << std::endl;
    std::cout << "Number of pairs: " << totalPairs << std::endl;
    std::cout << "Number of keys: " << dataMap->size() << std::endl;
    std::cout << "E[X^2] = " << expectedValueSquared << std::endl;

    return maxValues;
}

std::string getRandomKey(const std::vector<std::string>& vec) {
    if (vec.empty()) {
        throw std::runtime_error("Vector is empty");
    }

    // Random number generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, vec.size() - 1);

    // Select a random index
    int index = dis(gen);

    return vec[index];
}
void startProxy(LAT& lat, const string& data_size, const int& lambda) {
    std::cout << "Launching Proxy !" << std::endl;
    lat.LAT::SQPD_P_S(data_size, lambda);
}

void measureLatencyForKey(LAT& lat,const int lambda, const int Cid) {
    double waitTime;
    std::string randomKey;
    std::chrono::time_point<std::chrono::high_resolution_clock>start, end;
    vector<string> keysVec = lat.getKeys();
    //size_t thread_id_hash = std::hash<std::thread::id>()(std::this_thread::get_id());
    int warmUp = 1e2;
    int stop = 5e3 + warmUp;
   
    while (stop--) {

        if (Cid == 0 ) waitTime = exponentialWait(lambda);
		
        else waitTime = exponentialWait(lambda / 2.0);

       

        preciseSleep(waitTime); // Assuming waitTime is in seconds

        randomKey = getRandomKey(keysVec);


       // std::cout << "Client " << Cid <<" chosen keyword-----> " << randomKey << std::endl;

        //real vth
        lat.GetC_P(Cid, randomKey);


    }

}
bool spawnThreadsAndMeasure(const int numThreads, LAT& lat, std::string data_size, int lambda, int mrl) {
    std::vector<std::thread> threads;
	cout << "Spawning " << numThreads << " threads to measure latency." << std::endl;
    // Join any existing threads to ensure they are closed before starting new ones
    auto joinAllThreads = [&threads]() {
        for (auto& thread : threads) {
            if (thread.joinable()) {
                thread.join();
            }
        }
        threads.clear();
        };

    // Ensuring all threads are joined before exiting the function
    struct ThreadGuard {
        std::vector<std::thread>& threads;
        ~ThreadGuard() {
            for (auto& thread : threads) {
                if (thread.joinable()) {
                    thread.join();
                }
            }
        }
    };

    ThreadGuard guard{ threads };

    // Start proxy thread
    threads.push_back(std::thread(startProxy, std::ref(lat), std::ref(data_size), std::ref(lambda)));

    // Start latency measurement threads
    for (int i = 0; i < numThreads; ++i) {
        threads.push_back(std::thread(measureLatencyForKey, std::ref(lat), lambda, i));
    }

    return true;
}

// Function to fill a multimap with keys where the key's length follows a geometric distribution
std::unordered_map<std::string, std::vector<std::string>> createMapWithGeometricDistribution(int numKeys, double successProbability) {
    std::unordered_map<std::string, std::vector<std::string>> myMap;
    std::random_device rd;  // Non-deterministic random number generator
    std::mt19937 gen(rd()); // Seed the generator
    std::geometric_distribution<> d(successProbability); // Geometric distribution

    size_t nbrofpairs = 0;
    size_t maxlength = 0;

    for (int i = 0; i < numKeys; ++i) {
        // Generate a key name
        std::string key = "Key_" + std::to_string(i);

        // Generate a random size for the vector following the geometric distribution
        int vecSize = d(gen);

        // Create a vector of the determined size with dummy content
        std::vector<std::string> vec(vecSize, "dummy_value_1234567890123456789012345678901234567890123456789065324667866tutgf uyr65 765 541");
        if (maxlength < vecSize) {
            maxlength = vecSize;
        }
        nbrofpairs += vecSize;
        // Insert the key-value pair into the map
        myMap[key] = vec;
    }
    cout << "maxRep " << maxlength << "\n";
    cout << "number of pairs  " << nbrofpairs << "\n";

    return myMap;
}

int main() {

    for(int j = 4; j < 16; j *= 2)
    {
        for (int i = 14; i < 16; i += 2) {

            auto MM = std::make_unique<std::unordered_map<std::string, std::vector<std::string>>>(readAndMergeJSONFiles(input_directory, pow(2, i)));

            std::cout << j << " Reading MM " << i << " done" << std::endl;

            int maxResponseLength = printStatistics(MM.get());

            LAT lat("your_password_here", MM.get());

            MM.reset();

            spawnThreadsAndMeasure(2, lat, to_string(i), j, maxResponseLength);
        }
    }
    std::cout << "Press Enter to continue...";
    std::cin.get();  // Waits for the user to press Enter

    // Continue with the rest of your code
    std::cout << "Continuing with the rest of the program.\n";

    return 0;
}
