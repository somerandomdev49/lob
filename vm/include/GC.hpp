#pragma once
#include <cstdlib>
#include <forward_list>

#include "Object.hpp"

namespace Lob
{
    class GC
    {
    public:
        std::forward_list<ObjectPtr> &List;
        GC(std::forward_list<ObjectPtr> &list) : List(list) {}

        /** @brief Runs the garbage collector.
            @return Amount of objects sweeped. */
        std::size_t Run()
        {
            Mark(List.front());
            Sweep();
        }

    private:
        /** @brief Marks accessible objects. */
        void Mark(ObjectPtr o)
        {
            if(!o->Marked)
            {
                o->Marked = true;
                for (const auto &o : List)
                    Mark(o);
            }
        }

        /** @brief Sweeps unmarked objects.
            @return Amount of objects sweeped. */
        std::size_t Sweep()
        {
            std::size_t c = 0;
            for(const auto &o : List)
            {
                if(!o->Marked)
                    o->Finalize();
                else o->Marked = false;
                ++c;
            }
            return c;
        }
    };

}

