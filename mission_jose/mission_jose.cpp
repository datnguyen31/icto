#include "mission_jose.hpp"
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
    MissionTime.setEpoch(MISSION_JOSE_EPOCH_YEAR, MISSION_JOSE_EPOCH_MONTH, MISSION_JOSE_EPOCH_DAY,
                         MISSION_JOSE_EPOCH_HOUR, MISSION_JOSE_EPOCH_MINUTE, MISSION_JOSE_EPOCH_SECOND);

    // Load thread information from file
    if (!MissionExecutive.loadThreadsFromFile(MISSION_JOSE_THREAD_INFO))
    {
        std::cerr << "Failed to load threads from file" << std::endl;
        return 0;
    }

    if (MissionExecutive.createAll())
    {
        std::cout << "All threads created successfully" << std::endl;
    }
    else
    {
        std::cerr << "Failed to create all threads" << std::endl;
    }

    while (1)
    {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    // Clean up
    MissionExecutive.destroyAll();

    return 0;
}