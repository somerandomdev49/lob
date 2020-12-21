#pragma once
#include <iostream>
#include <stack>
#include <unordered_map>

#include "Instr.hpp"
#include "Object.hpp"

namespace Lob
{
    class VM
    {
        Scope scope;
        std::istream &in;


        void RunInstr()
        {
            switch(in.get()) {
                case InstrGetLocal:
                    if(!HasVar()) {
                        
                    }
            }
        }
    };
}
