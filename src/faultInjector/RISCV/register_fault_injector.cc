#include <fstream>
#include <iostream>

#include "register_fault_injector.hh"

namespace gem5 {

    RegisterFaultInjector::RegisterFaultInjector
        (const RegisterFaultInjectorParams &params) :
        SimObject(params),
        input_file(params.inputFile),
        number(params.number)   //initialization list
        {
            //std::cout << "Hello world, from a SimObject!" <<std::endl;
            std::cout << "Hey, I have a parameter: "
                << input_file << std::endl;
            std::cout << "Hey, I have a parameter: " << number << std::endl;
        }

    std::string RegisterFaultInjector::getString(void){
        return this->input_file;
    }

    int RegisterFaultInjector::getNumber(void){
        return this->number;
    }

    //no need to specify again static
    std::string RegisterFaultInjector::readFromFile
    (std::string filename){
        std::ifstream file(filename);

        if (!file){
            std::cout << "Error reading the file" << std::endl;
            return "Error";
        }

        std::string lines = "", line;

        while (std::getline(file, line)){
            lines += line;
        }

        file.close();
        return lines;
    }

    std::vector<unsigned int> RegisterFaultInjector::readMasks
    (std::string filename, int size, int type){
        std::vector<unsigned int> arr(size, 0);

        std::ifstream file(filename);
        std::string word;

        /*
        The file should be organized as a N * 2 matrix, where
        the first column is the id of the register and
        the second column is the mask corresponding to that specific register
        No need to specify a mask to all the registers.
        This file has to be stored in the same folder of the
        script calling the gem5.opt
        At this moment, the file has to be named "registerMasks.txt"
        */


        if (!file){
            std::cout << "Error reading the file registerMasks.txt"
                << std::endl;

            return arr;
        }

        std::cout << "Reading masks from file..." << std::endl;

        while (file >> word){
            //std::cout << word << std::endl;
            int index = std::stoi(word);
            file >> word;
            //std::cout << "Also: " << word << std::endl;
            int mask = std::stoi(word, 0, 16);

            file >> word;
            if (type==0 && word=="ST0"){
                arr[index] = mask;
            }
            if (type==1 && word=="ST1"){
                arr[index] = mask;
            }
            if (type==2 && word=="BITFLIP"){
                arr[index] = mask;
            }

        }

        return arr;
    }


    std::list<unsigned long>
        RegisterFaultInjector::readTimeIntervals(std::string filename){

        std::ifstream file(filename);
        std::string word;
        std::list<unsigned long> timeIntervals;

        /*
        The file should be organized as list of time instants (ticks).
        Supposing that the first line is line 1, the odd lines are the
        lower bounds of the intervals, while the even lines are the
        upper bounds.
        At this moment, the file has to be named "faultTimeIntervals.txt"
        */


        if (!file){
            std::cout << "Error reading the file faultTimeIntervals.txt"
                << std::endl;
            return timeIntervals;
        }

        std::cout << "Reading time intervals from file..." << std::endl;

        while (file >> word){
            timeIntervals.push_back(std::stol(word));
        }

        return timeIntervals;
    }

}
