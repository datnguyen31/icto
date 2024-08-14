#include "mission_sample.hpp"
#include "../ps/inc/platform_services.hpp"

#include <iostream>
#include <thread>

using namespace PlatformServices;

int main()
{
    // Create an instance of the MissionExecutive
    Executive MissionExecutive;

    // Create an instance of the TimeService
    TimeService& MissionTime = TimeService::getInstance();
    MissionTime.setEpoch(MISSION_SAMPLE_EPOCH_YEAR, MISSION_SAMPLE_EPOCH_MONTH,
                         MISSION_SAMPLE_EPOCH_DAY, MISSION_SAMPLE_EPOCH_HOUR,
                         MISSION_SAMPLE_EPOCH_MINUTE, MISSION_SAMPLE_EPOCH_SECOND);

    // Load thread information from file
    if (!MissionExecutive.loadThreadsFromFile(MISSION_SAMPLE_THREAD_INFO))
    {
        std::cerr << "Failed to load threads from file" << std::endl;
        return 0;
    }

    // Create and start both threads
    if (MissionExecutive.createAll())
    {
        std::cout << "Threads created successfully" << std::endl;
    }
    else
    {
        std::cerr << "Failed to create threads" << std::endl;
        return 0;
    }
    
    while (1)
    {
        std::this_thread::yield();
    }

    // Clean up
    MissionExecutive.destroyAll();

    return 0;
}