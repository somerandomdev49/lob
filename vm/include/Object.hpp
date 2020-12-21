#pragma once
#include <unordered_map>

namespace Lob
{
    class Object;

    using ObjectPtr = Object*;

    struct Object
    {
        /** @brief A map of object's fields.
            @note Might change to std::map. */
        std::unordered_map<std::string, ObjectPtr> Fields;

        /** @brief Whether the object is marked by GC */
        bool Marked = false;

        /** @brief Finalizes the object.
            @warning Object deletes itself, do not use
                     after calling this function. */
        void Finalize()
        { delete this; }
    };
}
