/*************************************************************************
 *   Copyright (C) 2009 by Renaud Guezennec                              *
 *                                                                       *
 *   https://rolisteam.org/                                           *
 *                                                                       *
 *   rolisteam is free software; you can redistribute it and/or modify   *
 *   it under the terms of the GNU General Public License as published   *
 *   by the Free Software Foundation; either version 2 of the License,   *
 *   or (at your option) any later version.                              *
 *                                                                       *
 *   This program is distributed in the hope that it will be useful,     *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of      *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       *
 *   GNU General Public License for more details.                        *
 *                                                                       *
 *   You should have received a copy of the GNU General Public License   *
 *   along with this program; if not, write to the                       *
 *   Free Software Foundation, Inc.,                                     *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.           *
 *************************************************************************/
#ifndef LISTALIASNODE_H
#define LISTALIASNODE_H

#include <diceparser/dicealias.h>

#include "executionnode.h"
#include "result/stringresult.h"

/**
 * @brief The ListAliasNode class is dedicated to display the list of the current aliases.
 */
class ListAliasNode : public ExecutionNode
{
public:
    ListAliasNode(const QList<DiceAlias*>& mapAlias);
    /**
     * @brief run
     * @param previous
     */
    virtual void run(ExecutionNode* previous= nullptr);

    /**
     * @brief toString
     * @return
     */
    virtual QString toString(bool) const;
    /**
     * @brief buildList
     * @return
     */
    virtual QString buildList() const;
    /**
     * @brief getPriority
     * @return
     */
    virtual qint64 getPriority() const;

    virtual ExecutionNode* getCopy() const;

private:
    const QList<DiceAlias*>& m_aliasList;
};

#endif // LISTALIASNODE_H
