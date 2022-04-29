/***************************************************************************
 * Copyright (C) 2014 by Renaud Guezennec                                   *
 * https://rolisteam.org/contact                                         *
 *                                                                          *
 *  This file is part of DiceParser                                         *
 *                                                                          *
 * This program is free software; you can redistribute it and/or modify     *
 * it under the terms of the GNU General Public License as published by     *
 * the Free Software Foundation; either version 2 of the License, or        *
 * (at your option) any later version.                                      *
 *                                                                          *
 * This program is distributed in the hope that it will be useful,          *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of           *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the             *
 * GNU General Public License for more details.                             *
 *                                                                          *
 * You should have received a copy of the GNU General Public License        *
 * along with this program; if not, write to the                            *
 * Free Software Foundation, Inc.,                                          *
 * 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.                 *
 ***************************************************************************/
#ifndef UNIQUENODE_H
#define UNIQUENODE_H

#include "node/executionnode.h"
#include "result/diceresult.h"

/**
 * @brief The UniqueNode class is an ExecutionNode. It is dedicated to unique result of one dice into one dimension array.
 */
class UniqueNode : public ExecutionNode
{
public:
    UniqueNode();
    void run(ExecutionNode* previous);
    virtual QString toString(bool withLabel) const;
    virtual qint64 getPriority() const;
    virtual ExecutionNode* getCopy() const;

private:
    DiceResult* m_diceResult;
};

#endif // NUMBERNODE_H
